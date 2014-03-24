# file: suck.py

# This is a parser to download, unpack, and process patent data from USPTO.

# usage on cli: ./manage.py suck <#no of weeks to process> <starting date in the form yyyymmdd>

# It works on dates newer or equal to 2005-01-04
# before this date, the format (xml keys) is different.
#
# The data format before the date 2002-01-01 is significantly different,
# data are stored in .txt files instead of .xml.
# The parser is not adapted to this format.

# details of format changes (and .dtd files):
# http://www.uspto.gov/products/xml-resources.jsp
#
# TODO: automatically delete .xml files after parsing

import os.path
import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

import urllib
import unzip
import os
import xmltodict

# using django data models
from sucker.models import Citation, Patent, Person, Claim

# Citation.objects.all().delete()

directory = settings.TEMP

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            number_of_weeks = int(args[0])
        except IndexError:
            number_of_weeks = 1
        try:
            start_date = datetime.datetime.strptime(args[1], '%Y%m%d').date()  # Year with century as a decimal number. Month [01,12]. Day [01,31].
        except IndexError:
            start_date = datetime.date(2013, 1, 1)  # default date

        # some changes in dtd happened on these dates:
        change_date_12 = datetime.date(2012, 12, 04)
        change_date_05 = datetime.date(2005, 1, 1)
        change_date_01 = datetime.date(2001, 1, 1)

        # switch for formats, numbers go from newest to oldest
        format = 0

        # same formats, different key names
        if start_date < change_date_12:
            parties = "parties"
            applicant_v = "applicant"
            applicants_v = "applicants"
            citation_v = "citation"
            references_cited = "references-cited"

        else:  # use the new names
            parties = "us-parties"
            applicant_v = "us-applicant"
            applicants_v = "us-applicants"
            citation_v = "us-citation"
            references_cited = "us-references-cited"

        # take care of the prefixes
        if start_date > change_date_05:
            prefix = ("ipg")

        # TODO: take care of .sgm files in year 2001, several changes happened, twice!

        elif start_date > change_date_01:
            prefix = ("pg") 
        else:
            raise Exception("date earlier than 2001-1-1, data in different format!")
            # it has this form: pftaps20000104_wk01.zip

        for week_no in xrange(number_of_weeks):
            week = start_date+datetime.timedelta(days=7*week_no)
            week_str = week.strftime("%y%m%d")

            # debugging
            print "week_str: %s" % (week_str, )
            
            week_zip = os.path.join(directory, "%s%s.zip" % (prefix, week_str))
            week_xml = os.path.join(directory, "%s%s.xml" % (prefix, week_str))

            # download
            if not os.path.exists(week_xml):
                url = "http://storage.googleapis.com/patents/grant_full_text/%s/%s%s.zip" % (week.year, prefix, week_str, )
                print url
                urllib.urlretrieve (url, week_zip)

                # unzip
                un = unzip.unzip()
                un.extract(week_zip, week_xml)

                # clean up
                os.remove(week_zip)

            # testing
            # filename = os.path.join(settings.TEMP, "development", "patents.xml")

            separator = '<?xml version="1.0"'
            for raw_xml, index in zip([separator+part for part in file(os.path.join(week_xml, "%s%s.xml" % (prefix, week_str))).read().split(separator)][1:], xrange(10**7)):

                # file(os.path.join(settings.TEMP, "%s.xml"%index), "w").write(raw_xml)
                xml = xmltodict.parse(raw_xml)

                if not xml.has_key("us-patent-grant"):
                    if xml.has_key("PATDOC"):
                        format = 1
                        #print "old format"

                    else:
                        print "E (%s): bad patent format" % (index, )
                        continue

                # parsing part
                #
                if format == 0:
                    # the newest format

                    # doc-number starting with 'D' are design patents that we want to filter out
                    if xml["us-patent-grant"]["us-bibliographic-data-grant"]["publication-reference"]["document-id"]["doc-number"].startswith('D'):
                        print "design patent"
                        continue

                    # debugging
                    print "processing patent"

                    patent_obj = Patent(
                         document_number=xml["us-patent-grant"]["us-bibliographic-data-grant"]["publication-reference"]["document-id"]["doc-number"],
                         publication_date=xml["us-patent-grant"]["us-bibliographic-data-grant"]["publication-reference"]["document-id"]["date"],
                         type=xml["us-patent-grant"]["us-bibliographic-data-grant"]["publication-reference"]["document-id"]["kind"],
                         country=xml["us-patent-grant"]["us-bibliographic-data-grant"]["publication-reference"]["document-id"]["country"],
                         application_number=xml["us-patent-grant"]["us-bibliographic-data-grant"]["application-reference"]["document-id"]["doc-number"],
                         application_date=xml["us-patent-grant"]["us-bibliographic-data-grant"]["application-reference"]["document-id"]["date"],
                         title=xml["us-patent-grant"]["us-bibliographic-data-grant"]["invention-title"]["#text"],
                        # title=xml["us-patent-grant"]["us-bibliographic-data-grant"]["invention-title"],
                    )
                    patent_obj.save()

                    claims = xml["us-patent-grant"]["claims"]["claim"]
                    if type(claims) != list:
                        claims = (claims, )

                    for claim in claims:
                        obj = Claim(
                            clm_id=claim["@id"],
                            text=claim["claim-text"],
                        )
                        obj.save()
                        patent_obj.claims.add(obj)

                    if not xml["us-patent-grant"]["us-bibliographic-data-grant"].has_key(parties):
                        print "E (%s): missing 'us-parties'" % (index, )
                    else:
                        us_parties = xml["us-patent-grant"]["us-bibliographic-data-grant"][parties]
                        try:  # inventors were not a mandatory element
                            inventors = us_parties["inventors"]["inventor"]
                            if type(inventors) != list:
                                inventors = (inventors, )

                            for inventor in inventors:
                                obj = Person(
                                    last_name=inventor["addressbook"].get("last-name", ""),
                                    first_name=inventor["addressbook"].get("first-name", ""),
                                    organization_name=inventor["addressbook"].get("orgname", ""),
                                    city=inventor["addressbook"]["address"]["city"],
                                    country=inventor["addressbook"]["address"]["country"],
                                )
                                obj.save()
                                patent_obj.inventors.add(obj)
                        except KeyError:
                            print "E (%s): missing 'inventors'" % (index, )

                        applicants = us_parties[applicants_v][applicant_v]
                        if type(applicants) != list:
                            applicants = (applicants, )

                        for applicant in applicants:
                            obj = Person(
                                last_name=applicant["addressbook"].get("last-name", ""),
                                first_name=applicant["addressbook"].get("first-name", ""),
                                organization_name=applicant["addressbook"].get("orgname", ""),
                                city=applicant["addressbook"]["address"]["city"],
                                country=applicant["addressbook"]["address"]["country"],
                            )
                            obj.save()
                            patent_obj.applicants.add(obj)

                    if not xml["us-patent-grant"]["us-bibliographic-data-grant"].has_key("assignees"):
                        print "E (%s): missing 'assignees'" % (index, )
                    else:
                        if xml["us-patent-grant"]["us-bibliographic-data-grant"].has_key(parties):
                            us_parties = xml["us-patent-grant"]["us-bibliographic-data-grant"][parties]
                            try:
                                inventors = us_parties["inventors"]["inventor"]
                            except KeyError:
                                print "E (%s): missing 'inventors'" % (index, )

                        assignees = xml["us-patent-grant"]["us-bibliographic-data-grant"]["assignees"]["assignee"]

                        if type(assignees) != list:
                            assignees = (assignees, )

                        for assignee in assignees:
                            try:
                                obj = Person(
                                    last_name=assignee["addressbook"].get("last-name", ""),
                                    first_name=assignee["addressbook"].get("first-name", ""),
                                    organization_name=assignee["addressbook"].get("orgname", ""),
                                    # TODO: city is sometime missing!
                                    city="",  
                                    country=assignee["addressbook"]["address"]["country"],
                                )
                                obj.save()
                            except KeyError:
                                print "E (%s): missing 'addressbook' for assignee" % (index, )

                    examiners = xml["us-patent-grant"]["us-bibliographic-data-grant"]["examiners"]
                    if not examiners.has_key("primary-examiner"):
                        print "E (%s): missing 'primary-examiner'" % (index, )
                    else:
                        obj = Person(
                            last_name=examiners["primary-examiner"]["last-name"],
                            first_name=examiners["primary-examiner"]["first-name"],
                        )
                        obj.save()
                        patent_obj.examiners.add(obj)
                    if not examiners.has_key("assistant-examiner"):
                        print "E (%s): missing 'assistant-examiner'" % (index, )
                    else:
                        obj = Person(
                            last_name=examiners["assistant-examiner"]["last-name"],
                            first_name=examiners["assistant-examiner"]["first-name"],
                        )
                        obj.save()
                        patent_obj.examiners.add(obj)

                    if not xml["us-patent-grant"]["us-bibliographic-data-grant"].has_key(references_cited):
                        print "E (%s): missing 'us-references-cited'" % (index, )
                    else:
                        us_references_cited = xml["us-patent-grant"]["us-bibliographic-data-grant"][references_cited]
                        citations = us_references_cited[citation_v]
                        for citation in citations:
                            if type(citation) != xmltodict.OrderedDict:
                                print "E (%s): bad-type 'citation'" % (index, )
                                continue
                            if not citation.has_key("patcit"):
                                continue
                            citation = citation["patcit"]["document-id"]
                            if not (citation.has_key("kind") and citation.has_key("name")):
                                continue
                            obj = Citation(
                                pubdate=citation["date"],
                                docnum=citation["doc-number"],
                                type=citation["kind"],
                                name=citation["name"],
                            )
                            obj.save()
                            patent_obj.citations.add(obj)

                    patent_obj.save()
                elif format == 1:
                    # TODO: process the data in the old format

                    # doc-number starting with 'D' are design patents that we need to filter out
                    if xml["PATDOC"]["SDOBI"]["B100"]["B110"]["DNUM"]["PDAT"].startswith('D'):
                        print "design patent"
                        continue

                    patent_obj = Patent(
                         document_number=xml["PATDOC"]["SDOBI"]["B100"]["B110"]["DNUM"]["PDAT"],
                         publication_date=xml["PATDOC"]["SDOBI"]["B100"]["B140"]["DATE"]["PDAT"],
                         type=xml["PATDOC"]["SDOBI"]["B100"]["B130"]["PDAT"],
                         country=xml["PATDOC"]["SDOBI"]["B100"]["B190"]["PDAT"],
                         application_number=xml["PATDOC"]["SDOBI"]["B200"]["B210"]["DNUM"]["PDAT"],
                         application_date=xml["PATDOC"]["SDOBI"]["B200"]["B220"]["DATE"]["PDAT"],
                         title=xml["PATDOC"]["SDOBI"]["B500"]["B540"]["STEXT"]["PDAT"],

                    )
                    patent_obj.save()

                    # debugging
                    print "processing"

                    claims = xml["PATDOC"]["SDOCL"]["CL"]
                    if type(claims) != list:
                        claims = (claims, )

                    patent_obj.save()
                #else
                #    raise Exception("unknown data format!")


            # clean up xml
#           os.removedirs(week_xml)