#!/usr/bin/env python3
"""Builds the Inheritance Tax Explained static site (Steve Hunt ACII TEP).

Output goes to site/out/. Every page is self-contained HTML with inline CSS,
plain semantic markup and JSON-LD, so that search engines and AI crawlers can
read the whole thing without running any JavaScript.

House rules built into this script:
- Every answer carries a Sources line. Each source is labelled Law, HMRC,
  Provider evidence, Published source, Steve's analysis or Steve's experience.
- The visible answers and their JSON-LD copies come from the same data, so
  they always change together.
- Transcripts record what is said in the videos and are never edited. Dated
  notes sit beside any words that need correcting or qualifying.
"""
import html
import json
import os
import re
from datetime import date

from guides import GUIDES as ALL_GUIDES, WOL_GUIDE_RELEASE

# Draft guides are built only when INCLUDE_DRAFTS=1, so a publishable build never links to an unapproved page.
INCLUDE_DRAFTS = os.environ.get("INCLUDE_DRAFTS") == "1"
GUIDES = [g for g in ALL_GUIDES if INCLUDE_DRAFTS or not g.get("draft")]

SITE = "https://inheritancetaxexplained.co.uk"
SITE_NAME = "Inheritance Tax Explained"
AUTHOR = "Steve Hunt ACII TEP"
LINKEDIN = "https://www.linkedin.com/in/steve~hunt"
YOUTUBE_CHANNEL = "https://www.youtube.com/@SteveHuntACIITEP"
X_PROFILE = "https://x.com/SHunt_ACII_TEP"
PLAYLIST = "https://www.youtube.com/playlist?list=PLYeD4F-FZfOA"
ABOUT_SLUG = "about-steve-hunt"
ABOUT_PATH = f"/{ABOUT_SLUG}/"
ABOUT_URL = f"{SITE}{ABOUT_PATH}"
ABOUT_PUBLISHED = "2026-10-03"
CII_TITLES = "https://www.cii.co.uk/about-us/professional-standards/using-cii-designations-and-titles/"
CIRM_REGISTER = "https://www.regulated-professions.service.gov.uk/professions/chartered-insurance-risk-manager"
STEP_SITE = "https://www.step.org/"
TODAY = date(2026, 10, 3)
WOL_GUIDE_SLUG = "whole-of-life-assurance/guide"
WOL_GUIDE_IN_BUILD = any(g["slug"] == WOL_GUIDE_SLUG for g in GUIDES)
if WOL_GUIDE_IN_BUILD:
    TODAY = date.fromisoformat(WOL_GUIDE_RELEASE)  # the home, about and corrections pages list the new guide
REVIEWED = date(2026, 10, 1)
AS_AT = "1 October 2026"
NOTE_DATE = "1 October 2026"
# Date of the consistency pass after Clara's release review (R01 to R08). New notes carry it;
# old notes keep NOTE_DATE and REVIEWED, which must not be moved on.
FIX_DATE = date(2026, 10, 3)
CORRECTIONS_SLUG = "sources-and-corrections"
CORRECTIONS_PATH = f"/{CORRECTIONS_SLUG}/"
CORRECTIONS_URL = f"{SITE}{CORRECTIONS_PATH}"
# Evidence extract for the nominees' annuity quotations. Draft until Clara has reviewed it and Steve says go:
# while EVIDENCE_DRAFT is True it is built only with INCLUDE_DRAFTS=1, and q_nominees stays "held on file".
EVIDENCE_SLUG = "nominees-annuity/quotations"
EVIDENCE_PATH = f"/{EVIDENCE_SLUG}/"
EVIDENCE_URL = f"{SITE}{EVIDENCE_PATH}"
EVIDENCE_DRAFT = False  # published 3 October 2026 on Steve's go
EVIDENCE_PUBLISHED = "2026-10-03"  # actual first publication date; never moves
INCLUDE_EVIDENCE = INCLUDE_DRAFTS or os.environ.get("INCLUDE_EVIDENCE") == "1" or not EVIDENCE_DRAFT
HOME_DESCRIPTION = ("Plain English videos and transcripts on UK inheritance tax, pensions from April 2027, "
                    "annuities and whole of life assurance. By Steve Hunt ACII TEP.")

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

ARTICLES = {
    "husband": (
        "Your Husband Left You A £500,000 Pension. It Could Cost Your Family £516,000 In Tax.",
        "https://www.linkedin.com/pulse/your-husband-left-you-500000-pension-could-cost-tax-steve-hunt-mjiae",
    ),
    "oneword": (
        "One Word Dragged £1 Trillion Into Inheritance Tax. One Clause Lets You Take Yours Back Out.",
        "https://www.linkedin.com/pulse/one-word-dragged-1-trillion-inheritance-tax-clause-steve-hunt-pepee",
    ),
    "jail": (
        "Osborne's Get Out of Jail Card Under Attack",
        "https://www.linkedin.com/pulse/osbornes-get-out-jail-card-under-attack-steve-hunt-0ddqe",
    ),
    "killed": (
        "George Osborne Killed The Annuity Market With One Sentence. He May Have Just Saved It With Another.",
        "https://www.linkedin.com/pulse/george-osborne-killed-annuity-market-one-sentence-he-steve-hunt-vi1gc",
    ),
    "certainties": (
        "There are two certainties in life: death and taxes. After forty-six years in pensions, I think there's a third.",
        "https://www.linkedin.com/pulse/two-certainties-life-death-taxes-after-forty-six-i-steve-hunt-5yfjf",
    ),
    "days86": (
        "86 days, 10 hours, 5 minutes and 42 seconds",
        "https://www.linkedin.com/pulse/86-days-10-hours-5-minutes-42-seconds-steve-hunt-i2kze",
    ),
    "pastor": (
        "The Pastor Who Tried to Prove God and Accidentally Predicted Death",
        "https://www.linkedin.com/pulse/pastor-who-tried-prove-god-accidentally-predicted-steve-hunt-tzase",
    ),
}

# ---------------------------------------------------------------------------
# Sources. Every link below was opened and checked on 1 October 2026.
# ---------------------------------------------------------------------------

LEG = "https://www.legislation.gov.uk"
TN = ("https://www.gov.uk/government/publications/inheritance-tax-on-pensions-technical-note/"
      "technical-note-inheritance-tax-on-pensions")
TN2 = ("https://www.gov.uk/government/publications/inheritance-tax-on-pensions-technical-note-2/"
       "technical-note-2-further-information-on-inheritance-tax-and-pensions")

LABEL_ORDER = ["Law", "Case law", "HMRC", "Provider evidence", "Published source", "Steve's analysis",
               "Steve's experience"]

LABEL_MEANING = {
    "Law": "the Act and section, linked to the official text on legislation.gov.uk",
    "Case law": "court judgments, linked to the published judgment",
    "HMRC": "HMRC's manuals, technical notes and GOV.UK guidance: HMRC's reading of the law, not the law itself",
    "Provider evidence": "real quotations and insurers' answers, dated and held on file, with no client information",
    "Published source": "figures and history credited to the publication that reported them",
    "Steve's analysis": "Steve's own reading or arithmetic, where it goes beyond settled law or HMRC's published view",
    "Steve's experience": "Steve's recollection of more than 45 years in UK financial services",
}

SOURCES = {
    # Law
    "ihta150A": ("Law", "Inheritance Tax Act 1984, s.150A", f"{LEG}/ukpga/1984/51/section/150A"),
    "fa2026s66": ("Law", "Finance Act 2026, s.66", f"{LEG}/ukpga/2026/11/section/66"),
    "fa2026s71": ("Law", "Finance Act 2026, s.71", f"{LEG}/ukpga/2026/11/section/71"),
    "ihta18": ("Law", "Inheritance Tax Act 1984, s.18", f"{LEG}/ukpga/1984/51/section/18"),
    "ihta8A": ("Law", "Inheritance Tax Act 1984, s.8A", f"{LEG}/ukpga/1984/51/section/8A"),
    "ihta8D": ("Law", "Inheritance Tax Act 1984, s.8D", f"{LEG}/ukpga/1984/51/section/8D"),
    "ihta3A": ("Law", "Inheritance Tax Act 1984, s.3A", f"{LEG}/ukpga/1984/51/section/3A"),
    "ihta7": ("Law", "Inheritance Tax Act 1984, s.7", f"{LEG}/ukpga/1984/51/section/7"),
    "ihta19": ("Law", "Inheritance Tax Act 1984, s.19", f"{LEG}/ukpga/1984/51/section/19"),
    "ihta21": ("Law", "Inheritance Tax Act 1984, s.21", f"{LEG}/ukpga/1984/51/section/21"),
    "ihta226": ("Law", "Inheritance Tax Act 1984, s.226", f"{LEG}/ukpga/1984/51/section/226"),
    "ihta233": ("Law", "Inheritance Tax Act 1984, s.233", f"{LEG}/ukpga/1984/51/section/233"),
    "ihta265": ("Law", "Inheritance Tax Act 1984, s.265", f"{LEG}/ukpga/1984/51/section/265"),
    "fa2004p27AA": ("Law", "Finance Act 2004, Sch. 28, para. 27AA", f"{LEG}/ukpga/2004/12/schedule/28/paragraph/27AA"),
    "fa2004p27A": ("Law", "Finance Act 2004, Sch. 28, para. 27A", f"{LEG}/ukpga/2004/12/schedule/28/paragraph/27A"),
    "fa2015": ("Law", "Finance Act 2015, Sch. 4, para. 3", f"{LEG}/ukpga/2015/11/schedule/4/paragraph/3"),
    "tpa2014": ("Law", "Taxation of Pensions Act 2014, Sch. 2, para. 3", f"{LEG}/ukpga/2014/30/schedule/2/paragraph/3"),
    "itepa646B": ("Law", "Income Tax (Earnings and Pensions) Act 2003, s.646B", f"{LEG}/ukpga/2003/1/section/646B"),
    "ita35": ("Law", "Income Tax Act 2007, s.35", f"{LEG}/ukpga/2007/3/section/35"),
    "nics2026": ("Law", "National Insurance Contributions (Employer Pensions Contributions) Act 2026, s.1",
                 f"{LEG}/ukpga/2026/15/section/1"),
    "laa1774": ("Law", "Life Assurance Act 1774", f"{LEG}/apgb/Geo3/14/48"),
    "cpa253": ("Law", "Civil Partnership Act 2004, s.253", f"{LEG}/ukpga/2004/33/section/253"),
    "fsa1986": ("Law", "Financial Services Act 1986 (since repealed)", f"{LEG}/ukpga/1986/60/contents"),
    "si1988": ("Law", "Financial Services Act 1986 (Commencement) (No. 8) Order 1988", f"{LEG}/uksi/1988/740/made"),
    # HMRC
    "tn": ("HMRC", "HMRC technical note: Inheritance Tax on pensions (updated 29 May 2026)", TN),
    "tn22": ("HMRC", "HMRC technical note, 2.2 Liability for Inheritance Tax", TN + "#liability-for-inheritance-tax"),
    "tn331": ("HMRC", "HMRC technical note, 3.3.1 Dependants' scheme pension", TN + "#dependants-scheme-pension"),
    "tn333": ("HMRC", "HMRC technical note, 3.3.3 Joint life annuities", TN + "#joint-life-annuities"),
    "tn334": ("HMRC", "HMRC technical note, 3.3.4 Death in service benefits", TN + "#death-in-service-benefits"),
    "tn34": ("HMRC", "HMRC technical note, 3.4 Exempt beneficiaries", TN + "#exempt-beneficiaries"),
    "tn7": ("HMRC", "HMRC technical note, 7 Pensions direct payment scheme", TN + "#pensions-direct-payment-scheme"),
    "tn1121": ("HMRC", "HMRC technical note, 11.2.1 Loss on sale", TN + "#loss-on-sale"),
    "tn1123": ("HMRC", "HMRC technical note, 11.2.3 Business and agricultural property relief",
               TN + "#business-property-relief-and-agricultural-property-relief"),
    "tn1124": ("HMRC", "HMRC technical note, 11.2.4 Instalments", TN + "#instalments"),
    "tn1125": ("HMRC", "HMRC technical note, 11.2.5 Lifetime transfers",
               TN + "#lifetime-transfers-and-normal-expenditure-out-of-income-exemption"),
    "ptm072210": ("HMRC", "HMRC Pensions Tax Manual, PTM072210",
                  "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm072210"),
    "ptm072200": ("HMRC", "HMRC Pensions Tax Manual, PTM072200",
                  "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm072200"),
    "rnrb": ("HMRC", "HMRC guidance: the residence nil rate band",
             "https://www.gov.uk/guidance/inheritance-tax-residence-nil-rate-band"),
    "inherit": ("HMRC", "GOV.UK: Tax on a private pension you inherit", "https://www.gov.uk/tax-on-pension-death-benefits"),
    "payiht": ("HMRC", "GOV.UK: Pay your Inheritance Tax bill", "https://www.gov.uk/paying-inheritance-tax"),
    "ihtgov": ("HMRC", "GOV.UK: How Inheritance Tax works", "https://www.gov.uk/inheritance-tax"),
    "itrates": ("HMRC", "GOV.UK: Income Tax rates and Personal Allowances", "https://www.gov.uk/income-tax-rates"),
    # Provider evidence (dated, held on file, not published)
    "q_nominees": ("Provider evidence", "Quotations from Just (11 August 2026) and Canada Life (10 August 2026), held on file", None),
    "q_age40": ("Provider evidence", "Insurers' answers on the nominee's age, August 2026, held on file", None),
    "q_wol": ("Provider evidence", "Whole of life quotation obtained in 2026, held on file", None),
    "q_just_doc": ("Provider evidence", "Just Retirement Limited, Pension Annuity Personal Quotation, 11 August 2026, "
                   "held on file", None),
    "q_cl_doc": ("Provider evidence", "Canada Life Limited, Your Lifetime Annuity Quotation, 10 August 2026, "
                 "held on file", None),
    "q_just_aug": ("Provider evidence", "Just correspondence, 8 and 11 August 2026: the request, the basis of the "
                   "figures and permission to publish them, held on file", None),
    "q_just_sep": ("Provider evidence", "Just correspondence, 14 September 2026: the dependant label and the "
                   "nomination, held on file", None),
    "q_cl_aug": ("Provider evidence", "Canada Life correspondence, 4 to 10 August 2026: the request, the basis of "
                 "the quotation and permission to name Canada Life, held on file", None),
    "q_cl_sep": ("Provider evidence", "Canada Life correspondence, 15 September 2026: the nominee age condition, "
                 "held on file", None),
    "just_terms": ("Provider evidence", "Just: Terms of the Pension Annuity, conditions 3.1 and 6.2.1 (published "
                   "conditions, retrieved 3 October 2026)",
                   "https://www.justadviser.com/globalassets/just-adviser/documents/"
                   "729-terms-of-the-just-retirement-pension-annuity.pdf"),
    # Published sources
    "pa1trn": ("Published source",
               "Pensions Age, 23 October 2025: DC pension assets quadruple to £1.2trn (Pensions Policy Institute, DC Future Book)",
               "https://www.pensionsage.com/pa/DC-pension-asets-quadruple-growth-remains-vulnerable.php"),
    "fos": ("Published source", "Financial Ombudsman Service: whole-of-life policies",
            "https://www.financial-ombudsman.org.uk/businesses/resolving-complaint/complaints-deal/investments/whole-life-policies"),
    "mg": ("Published source", "M&G Tech Matters: why life assurance policies require insurable interest",
           "https://www.mandg.com/wealth/adviser-services/tech-matters/investments-and-taxation/taxation-of-investment-bonds/life-assurance-insurable-interest"),
    "dnb": ("Published source", "Dictionary of National Biography (1885 to 1900): Dodson, James",
            "https://en.wikisource.org/wiki/Dictionary_of_National_Biography,_1885-1900/Dodson,_James"),
    "actuary": ("Published source", "The Actuary magazine, April 2024: The history of actuarial science",
                "https://www.theactuarymagazine.org/the-history-of-actuarial-science/"),
    # Steve
    "steve_pet": ("Steve's analysis", "Osborne's Get Out of Jail Card Under Attack (LinkedIn article)", ARTICLES["jail"][1]),
    "ihta3": ("Law", "Inheritance Tax Act 1984, s.3", f"{LEG}/ukpga/1984/51/section/3"),
    "ihta5": ("Law", "Inheritance Tax Act 1984, s.5", f"{LEG}/ukpga/1984/51/section/5"),
    "ihta151": ("Law", "Inheritance Tax Act 1984, s.151 (showing the 2027 changes)", f"{LEG}/ukpga/1984/51/section/151"),
    "ihta151old": ("Law", "Inheritance Tax Act 1984, s.151 as in force until 5 April 2027", f"{LEG}/ukpga/1984/51/section/151/2011-07-19"),
    "ihta272": ("Law", "Inheritance Tax Act 1984, s.272", f"{LEG}/ukpga/1984/51/section/272"),
    "fa2026s69": ("Law", "Finance Act 2026, s.69", f"{LEG}/ukpga/2026/11/section/69"),
    "fa2004p15": ("Law", "Finance Act 2004, Sch. 28, para. 15", f"{LEG}/ukpga/2004/12/schedule/28/paragraph/15"),
    "tn322": ("HMRC", "HMRC technical note, 3.2.2 (guarantee payments)", TN + "#defined-benefit-arrangements"),
    "ihtm17041": ("HMRC", "HMRC Inheritance Tax Manual, IHTM17041",
                  "https://www.gov.uk/hmrc-internal-manuals/inheritance-tax-manual/ihtm17041"),
    "ihtm17070": ("HMRC", "HMRC Inheritance Tax Manual, IHTM17070",
                  "https://www.gov.uk/hmrc-internal-manuals/inheritance-tax-manual/ihtm17070"),
    "ihtm20375": ("HMRC", "HMRC Inheritance Tax Manual, IHTM20375 (Statement of Practice E4)",
                  "https://www.gov.uk/hmrc-internal-manuals/inheritance-tax-manual/ihtm20375"),
    "iht403": ("HMRC", "GOV.UK: form IHT403, gifts and other transfers of value",
               "https://www.gov.uk/government/publications/inheritance-tax-gifts-and-other-transfers-of-value-iht403"),
    "iht409": ("HMRC", "GOV.UK: form IHT409, pensions",
               "https://www.gov.uk/government/publications/inheritance-tax-pensions-iht409"),
    "q_sept": ("Provider evidence", "Annuity quotations run on 19 September 2026, held on file", None),
    "ptm071200": ("HMRC", "HMRC Pensions Tax Manual, PTM071200 (definition of dependant)",
                  "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm071200"),
    "iht400notes": ("HMRC", "HMRC IHT400 Notes (April 2026), pages 30 to 31",
                    "https://assets.publishing.service.gov.uk/media/69cd0ecfb5210036050bc61f/IHT400_2022__Notes_04-26final.pdf"),
    "gifts": ("HMRC", "GOV.UK: Work out Inheritance Tax due on gifts", "https://www.gov.uk/guidance/work-out-inheritance-tax-due-on-gifts"),
    "salsac": ("HMRC", "GOV.UK: Salary sacrifice reform for pension contributions from 6 April 2029",
               "https://www.gov.uk/government/publications/salary-sacrifice-reform-for-pension-contributions-effective-from-6-april-2029/salary-sacrifice-reform-for-pension-contributions"),
    "parry": ("Case law", "HMRC v Parry and others [2020] UKSC 35 (Supreme Court)", "https://supremecourt.uk/cases/uksc-2018-0208"),
    "ihta263": ("Law", "Inheritance Tax Act 1984, s.263", f"{LEG}/ukpga/1984/51/section/263"),
    "ihta268": ("Law", "Inheritance Tax Act 1984, s.268", f"{LEG}/ukpga/1984/51/section/268"),
    "ihtm20211": ("HMRC", "HMRC Inheritance Tax Manual, IHTM20211 (a policy on the deceased's own life, not in trust)",
                  "https://www.gov.uk/hmrc-internal-manuals/inheritance-tax-manual/ihtm20211"),
    "pensions_example": ("Steve's analysis", "The worked example on the pensions page, with its assumptions",
                         f"{SITE}/pensions-and-inheritance-tax-from-april-2027/#key-facts"),
    # Added for the pensions guide (each opened and checked on 2 October 2026)
    "fa2026s67": ("Law", "Finance Act 2026, s.67", f"{LEG}/ukpga/2026/11/section/67"),
    "fa2026s68": ("Law", "Finance Act 2026, s.68", f"{LEG}/ukpga/2026/11/section/68"),
    "fa2026s70": ("Law", "Finance Act 2026, s.70", f"{LEG}/ukpga/2026/11/section/70"),
    "fa2026s72": ("Law", "Finance Act 2026, s.72", f"{LEG}/ukpga/2026/11/section/72"),
    "fa2021s86": ("Law", "Finance Act 2021, s.86", f"{LEG}/ukpga/2021/26/section/86"),
    "ihta23": ("Law", "Inheritance Tax Act 1984, s.23", f"{LEG}/ukpga/1984/51/section/23"),
    "ihta141": ("Law", "Inheritance Tax Act 1984, s.141", f"{LEG}/ukpga/1984/51/section/141"),
    "ihta226A": ("Law", "Inheritance Tax Act 1984, s.226A", f"{LEG}/ukpga/1984/51/section/226A"),
    "ihta226B": ("Law", "Inheritance Tax Act 1984, s.226B", f"{LEG}/ukpga/1984/51/section/226B"),
    "ihtasch1A": ("Law", "Inheritance Tax Act 1984, Sch. 1A", f"{LEG}/ukpga/1984/51/schedule/1A"),
    "itepa567B": ("Law", "Income Tax (Earnings and Pensions) Act 2003, s.567B", f"{LEG}/ukpga/2003/1/section/567B"),
    "fa2004s151": ("Law", "Finance Act 2004, s.151", f"{LEG}/ukpga/2004/12/section/151"),
    "ihtm17051": ("HMRC", "HMRC Inheritance Tax Manual, IHTM17051",
                  "https://www.gov.uk/hmrc-internal-manuals/inheritance-tax-manual/ihtm17051"),
    "ihtm17052": ("HMRC", "HMRC Inheritance Tax Manual, IHTM17052",
                  "https://www.gov.uk/hmrc-internal-manuals/inheritance-tax-manual/ihtm17052"),
    "tn12": ("HMRC", "HMRC technical note, 1.2 When does this change come into effect?",
             TN + "#when-does-this-change-come-into-effect"),
    "tn21": ("HMRC", "HMRC technical note, 2.1 When notional pension property is vested in a beneficiary",
             TN + "#when-notional-pension-property-is-vested-in-a-beneficiary"),
    "tn23": ("HMRC", "HMRC technical note, 2.3 Collection of Inheritance Tax", TN + "#collection-of-inheritance-tax"),
    "tn25": ("HMRC", "HMRC technical note, 2.5 Identifying pensions", TN + "#identifying-pensions"),
    "tn26": ("HMRC", "HMRC technical note, 2.6 Qualifying non-UK pension schemes and section 615(3) schemes",
             TN + "#qualifying-non-uk-pension-schemes-and-section-6153-schemes"),
    "tn321": ("HMRC", "HMRC technical note, 3.2.1 Money purchase arrangements", TN + "#money-purchase-arrangements"),
    "tn332": ("HMRC", "HMRC technical note, 3.3.2 Trivial commutation", TN + "#trivial-commutation"),
    "tn351": ("HMRC", "HMRC technical note, 3.5.1 Long-term and non-long-term UK residents",
              TN + "#long-term-and-non-long-term-uk-residents"),
    "tn4": ("HMRC", "HMRC technical note, 4 Valuations", TN + "#valuations"),
    "tn522": ("HMRC", "HMRC technical note, 5.2.2 Valuation information and timing",
              TN + "#valuation-information-and-timing"),
    "tn6": ("HMRC", "HMRC technical note, 6 Withholding", TN + "#withholding"),
    "tn732": ("HMRC", "HMRC technical note, 7.3.2 What should be included in a valid notice",
              TN + "#what-should-be-included-in-a-valid-notice-1"),
    "tn74": ("HMRC", "HMRC technical note, 7.4 Deducting Inheritance Tax from benefits",
             TN + "#deducting-inheritance-tax-from-benefits"),
    "tn8": ("HMRC", "HMRC technical note, 8 Income Tax on death benefits from pensions",
            TN + "#income-tax-on-death-benefits-from-pensions"),
    "tn82": ("HMRC", "HMRC technical note, 8.2 Reducing taxable pension income", TN + "#reducing-taxable-pension-income"),
    "tn10": ("HMRC", "HMRC technical note, 10 Probate and discharge certificates",
             TN + "#probate-and-discharge-certificates"),
    "tn111": ("HMRC", "HMRC technical note, 11.1 Charities and the general component",
              TN + "#charities-and-the-general-component"),
    "tn1122": ("HMRC", "HMRC technical note, 11.2.2 Quick succession relief", TN + "#quick-succession-relief"),
    "steve_p3": ("Steve's analysis", "Your Husband Left You A £500,000 Pension. It Could Cost Your Family £516,000 In Tax. (LinkedIn article)",
                 ARTICLES["husband"][1]),
    # Added after Clara's review of guide 2 (each opened and checked on 2 October 2026)
    "si2026818": ("Law", "SI 2026/818, the Registered Pension Schemes (Provision of Information) (Miscellaneous "
                  "Amendments) Regulations 2026", "https://www.legislation.gov.uk/uksi/2026/818/made"),
    "fa1986s102": ("Law", "Finance Act 1986, s.102", f"{LEG}/ukpga/1986/41/section/102"),
    "tn2_ex1": ("HMRC", "HMRC technical note 2 (27 August 2026), example 1: an annuity that ceased on death",
                TN2 + "#introduction"),
    "tn2_basic": ("HMRC", "HMRC technical note 2, 4.1 Basic information sharing requirements", TN2 + "#introduction-1"),
    "tn2_pexempt": ("HMRC", "HMRC technical note 2, 4.3 The basic information: reporting potentially exempt "
                    "beneficiaries", TN2 + "#the-basic-information--reporting-potentially-exempt-beneficiaries"),
    "tn2_further": ("HMRC", "HMRC technical note 2, 6 Further information: when an Inheritance Tax account is required",
                    TN2 + "#further-information--when-an-inheritance-tax-account-is-required"),
    "tn2_dsp": ("HMRC", "HMRC technical note 2, Dependants' scheme pensions", TN2 + "#dependants-scheme-pensions"),
    "tn2_deferment": ("HMRC", "HMRC technical note 2, Death in deferment", TN2 + "#death-in-deferment"),
    "tn2_beneficiary": ("HMRC", "HMRC technical note 2, Death of a beneficiary (example 8)", TN2 + "#death-of-a-beneficiary"),
    "tn2_amount": ("HMRC", "HMRC technical note 2, 7.6 Amount withheld", TN2 + "#amount-withheld"),
    "tn2_validity": ("HMRC", "HMRC technical note 2, 8.2 Validity of a payment notice", TN2 + "#validity-of-a-payment-notice"),
    "ihtm05120": ("HMRC", "HMRC Inheritance Tax Manual, IHTM05120 (postponing payment of tax)",
                  "https://www.gov.uk/hmrc-internal-manuals/inheritance-tax-manual/ihtm05120"),
    "ihtm45009": ("HMRC", "HMRC Inheritance Tax Manual, IHTM45009 (the baseline amount for the 36% rate)",
                  "https://www.gov.uk/hmrc-internal-manuals/inheritance-tax-manual/ihtm45009"),
    "ptm072430": ("HMRC", "HMRC Pensions Tax Manual, PTM072430 (beneficiaries' drawdown and income tax)",
                  "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm072430"),
    "ptm073400": ("HMRC", "HMRC Pensions Tax Manual, PTM073400 (annuity protection lump sum death benefit)",
                  "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm073400"),
    "ptm073700": ("HMRC", "HMRC Pensions Tax Manual, PTM073700 (trivial commutation lump sum death benefit)",
                  "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm073700"),
    "ptm073900": ("HMRC", "HMRC Pensions Tax Manual, PTM073900 (charity lump sum death benefit)",
                  "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm073900"),
    "ppi2025": ("Published source", "Pensions Policy Institute: The DC Future Book 2025",
                "https://www.pensionspolicyinstitute.org.uk/media/x3tjj4od/20251021-the-dc-future-book-final.pdf"),
    "steve_p1": ("Steve's analysis", "George Osborne Killed The Annuity Market With One Sentence (LinkedIn article)", ARTICLES["killed"][1]),
    "steve_p2": ("Steve's analysis", "One Word Dragged £1 Trillion Into Inheritance Tax (LinkedIn article)", ARTICLES["oneword"][1]),
    "steve_example": ("Steve's analysis", "The worked example: arithmetic on the stated assumptions", None),
    "steve_history": ("Steve's experience", "Steve Hunt, in UK financial services since 1980", None),
}


# Added for the whole of life guide (guide 3). Each link opened and checked on 4 October 2026.
IHTM = "https://www.gov.uk/hmrc-internal-manuals/inheritance-tax-manual/"
LAWCOM_II = ("https://cdn.websitebuilder.service.justice.gov.uk/uploads/sites/54/2026/01/"
             "cp201_extract_insurable_interest.pdf")
LAWCOM_II_NAME = "Law Commission: Insurable interest, the current law (consultation paper 201, Part 11, reissued 2015)"
SOURCES.update({
    # Law
    "ihta5_4": ("Law", "Inheritance Tax Act 1984, s.5(4)", f"{LEG}/ukpga/1984/51/section/5"),
    "ihta20": ("Law", "Inheritance Tax Act 1984, s.20", f"{LEG}/ukpga/1984/51/section/20"),
    "ihta21_134": ("Law", "Inheritance Tax Act 1984, s.21(1), (3) and (4)", f"{LEG}/ukpga/1984/51/section/21"),
    "ihta21_2": ("Law", "Inheritance Tax Act 1984, s.21(2)", f"{LEG}/ukpga/1984/51/section/21"),
    "ihta43": ("Law", "Inheritance Tax Act 1984, s.43", f"{LEG}/ukpga/1984/51/section/43"),
    "ihta58": ("Law", "Inheritance Tax Act 1984, s.58", f"{LEG}/ukpga/1984/51/section/58"),
    "ihta64": ("Law", "Inheritance Tax Act 1984, s.64", f"{LEG}/ukpga/1984/51/section/64"),
    "ihta65": ("Law", "Inheritance Tax Act 1984, s.65", f"{LEG}/ukpga/1984/51/section/65"),
    "ihta66": ("Law", "Inheritance Tax Act 1984, s.66", f"{LEG}/ukpga/1984/51/section/66"),
    "ihta67": ("Law", "Inheritance Tax Act 1984, s.67", f"{LEG}/ukpga/1984/51/section/67"),
    "ihta68": ("Law", "Inheritance Tax Act 1984, s.68", f"{LEG}/ukpga/1984/51/section/68"),
    "ihta69": ("Law", "Inheritance Tax Act 1984, s.69", f"{LEG}/ukpga/1984/51/section/69"),
    "ihta160": ("Law", "Inheritance Tax Act 1984, s.160", f"{LEG}/ukpga/1984/51/section/160"),
    "ihta167": ("Law", "Inheritance Tax Act 1984, s.167", f"{LEG}/ukpga/1984/51/section/167"),
    "ihta167_15": ("Law", "Inheritance Tax Act 1984, s.167, particularly s.167(1) and (5)",
                   f"{LEG}/ukpga/1984/51/section/167"),
    "ihtasch1": ("Law", "Inheritance Tax Act 1984, Sch. 1", f"{LEG}/ukpga/1984/51/schedule/1"),
    "mwpa11": ("Law", "Married Women's Property Act 1882, s.11", f"{LEG}/ukpga/Vict/45-46/75/section/11"),
    "cpa70": ("Law", "Civil Partnership Act 2004, s.70", f"{LEG}/ukpga/2004/33/section/70"),
    "cidra1to5": ("Law", "Consumer Insurance (Disclosure and Representations) Act 2012, ss.1 to 5",
                  f"{LEG}/ukpga/2012/6/contents"),
    "cidrasch1": ("Law", "Consumer Insurance (Disclosure and Representations) Act 2012, Sch. 1",
                  f"{LEG}/ukpga/2012/6/schedule/1"),
    "ittoia484": ("Law", "Income Tax (Trading and Other Income) Act 2005, s.484", f"{LEG}/ukpga/2005/5/section/484"),
    "ittoia485": ("Law", "Income Tax (Trading and Other Income) Act 2005, s.485", f"{LEG}/ukpga/2005/5/section/485"),
    "ittoia493": ("Law", "Income Tax (Trading and Other Income) Act 2005, s.493", f"{LEG}/ukpga/2005/5/section/493"),
    "tcga210": ("Law", "Taxation of Chargeable Gains Act 1992, s.210", f"{LEG}/ukpga/1992/12/section/210"),
    "icta266": ("Law", "Income and Corporation Taxes Act 1988, s.266(3)(c)", f"{LEG}/ukpga/1988/1/section/266"),
    "mlr45": ("Law", "Money Laundering Regulations 2017, reg. 45", f"{LEG}/uksi/2017/692/regulation/45"),
    "mlr45ZA": ("Law", "Money Laundering Regulations 2017, reg. 45ZA", f"{LEG}/uksi/2017/692/regulation/45ZA"),
    "mlrsch3A": ("Law", "Money Laundering Regulations 2017, Sch. 3A, paras 4 and 8", f"{LEG}/uksi/2017/692/schedule/3A"),
    # HMRC
    "ihtm14180": ("HMRC", "HMRC Inheritance Tax Manual, IHTM14180 (small gifts)", IHTM + "ihtm14180"),
    "ihtm14235": ("HMRC", "HMRC Inheritance Tax Manual, IHTM14235 (normal expenditure: life policy linked with an annuity)",
                  IHTM + "ihtm14235"),
    "ihtm14241": ("HMRC", "HMRC Inheritance Tax Manual, IHTM14241 (the meaning of normal)", IHTM + "ihtm14241"),
    "ihtm14242": ("HMRC", "HMRC Inheritance Tax Manual, IHTM14242 (a pattern of expenditure)", IHTM + "ihtm14242"),
    "ihtm14244": ("HMRC", "HMRC Inheritance Tax Manual, IHTM14244 (HMRC's account of the case Bennett v IRC [1995])",
                  IHTM + "ihtm14244"),
    "ihtm14250": ("HMRC", "HMRC Inheritance Tax Manual, IHTM14250 (out of income)", IHTM + "ihtm14250"),
    "ihtm14255": ("HMRC", "HMRC Inheritance Tax Manual, IHTM14255 (standard of living)", IHTM + "ihtm14255"),
    "ihtm16030": ("HMRC", "HMRC Inheritance Tax Manual, IHTM16030 (what is a trust?)", IHTM + "ihtm16030"),
    "ihtm20012": ("HMRC", "HMRC Inheritance Tax Manual, IHTM20012 (life policies and Inheritance Tax)", IHTM + "ihtm20012"),
    "ihtm20029": ("HMRC", "HMRC Inheritance Tax Manual, IHTM20029 (form IHT410 enquiries: open market value)",
                  IHTM + "ihtm20029"),
    "ihtm20045": ("HMRC", "HMRC Inheritance Tax Manual, IHTM20045 (premiums paid for someone else's benefit)",
                  IHTM + "ihtm20045"),
    "ihtm20241": ("HMRC", "HMRC Inheritance Tax Manual, IHTM20241 (the section 167 special rule)", IHTM + "ihtm20241"),
    "ihtm20251": ("HMRC", "HMRC Inheritance Tax Manual, IHTM20251 (a policy for someone else from the start)",
                  IHTM + "ihtm20251"),
    "ihtm20374": ("HMRC", "HMRC Inheritance Tax Manual, IHTM20374 (life policy linked with an annuity: the statutory position)", IHTM + "ihtm20374"),
    "ihtm20376": ("HMRC", "HMRC Inheritance Tax Manual, IHTM20376 (annuity and policy issued by different companies)", IHTM + "ihtm20376"),
    "ihtm42081": ("HMRC", "HMRC Inheritance Tax Manual, IHTM42081 (ten-year anniversary: introduction)", IHTM + "ihtm42081"),
    "iptm3515": ("HMRC", "HMRC Insurance Policyholder Taxation Manual, IPTM3515 (the value of a policy on death)",
                 "https://www.gov.uk/hmrc-internal-manuals/insurance-policyholder-taxation-manual/iptm3515"),
    "trsm23010": ("HMRC", "HMRC Trust Registration Service Manual, TRSM23010 (excluded express trusts: introduction)",
                  "https://www.gov.uk/hmrc-internal-manuals/trust-registration-service-manual/trsm23010"),
    "trsm23030": ("HMRC", "HMRC Trust Registration Service Manual, TRSM23030 (excluded express trusts: insurance policies)",
                  "https://www.gov.uk/hmrc-internal-manuals/trust-registration-service-manual/trsm23030"),
    "iht410": ("HMRC", "GOV.UK: form IHT410, life assurance and annuities",
               "https://www.gov.uk/government/publications/inheritance-tax-life-assurance-and-annuities-iht410"),
    "govtrusts": ("HMRC", "GOV.UK: Trusts and Inheritance Tax", "https://www.gov.uk/guidance/trusts-and-inheritance-tax"),
    "govtrusts2": ("HMRC", "GOV.UK: Trusts and taxes, Trusts and Inheritance Tax",
                   "https://www.gov.uk/trusts-taxes/trusts-and-inheritance-tax"),
    # Provider evidence (held on file, not published)
    "q_wol_aug": ("Provider evidence", "Indicative standard-rate whole of life comparison, 10 August 2026, "
                  "non-underwritten and nil commission, held on file (the calculations use the stated monthly "
                  "premium)", None),
    # Published sources
    "mh_life": ("Published source", "MoneyHelper: What is life insurance?",
                "https://www.moneyhelper.org.uk/en/everyday-money/insurance/what-is-life-insurance"),
    "mh_trust": ("Published source", "MoneyHelper: How to get your finances in order before you die",
                 "https://www.moneyhelper.org.uk/en/family-and-care/death-and-bereavement/"
                 "putting-your-financial-affairs-in-order-if-you-get-ill-or-die-making-a-will-and-more"),
    "lawcom_ii_7": ("Published source", LAWCOM_II_NAME + ", paras 11.72 to 11.75 (Reed v Royal Exchange "
                    "Assurance (1795) and Griffiths v Fleming [1909], cited at para 11.72)", LAWCOM_II),
    "lawcom_ii_8": ("Published source", LAWCOM_II_NAME + ", paras 11.73 to 11.76, citing Halford v Kymer (1830)",
                    LAWCOM_II),
    "lawcom_ii_9": ("Published source", LAWCOM_II_NAME + ", para 11.36, citing Dalby v India and London Life "
                    "Assurance Company (1854)", LAWCOM_II),
    "lawcom_proj": ("Published source", "Law Commission: Insurable interest project page",
                    "https://lawcom.gov.uk/project/insurance-contract-law-insurable-interest/"),
    "fca_ppc": ("Published source", "FCA Handbook Glossary: pure protection contract",
                "https://www.handbook.fca.org.uk/handbook/glossary/G935.html"),
    "fca_perg": ("Published source", "FCA Perimeter Guidance, PERG 2 Annex 2 (regulated activities and contracts of "
                 "insurance)", "https://www.handbook.fca.org.uk/handbook/PERG/2/Annex2.html"),
    "mh_o50": ("Published source", "MoneyHelper: Life insurance for over 50s",
               "https://www.moneyhelper.org.uk/en/family-and-care/death-and-bereavement/"
               "over-50s-life-insurance-is-it-worth-it"),
    "fscs_ins": ("Published source", "Financial Services Compensation Scheme: Insurance",
                 "https://www.fscs.org.uk/what-we-cover/insurance/"),
    "fca_dearceo22": ("Published source", "FCA: Dear CEO letter to life insurers, 14 December 2022",
                      "https://www.fca.org.uk/publication/correspondence/"
                      "dear-ceo-letter-expectations-life-insurers-cost-of-living.pdf"),
    "fca_pri23": ("Published source", "FCA: Insurance market priorities 2023 to 2025, 20 September 2023",
                  "https://www.fca.org.uk/publication/correspondence/life-insurance-market-priorities-2023.pdf"),
    "hansard1984": ("Published source", "Hansard, House of Commons, 13 March 1984: Budget statement, savings and "
                    "investment", "https://api.parliament.uk/historic-hansard/commons/1984/mar/13/savings-and-investment"),
    "ch_abbey": ("Published source", "Companies House: Abbey Life Assurance Company Limited (00710383)",
                 "https://find-and-update.company-information.service.gov.uk/company/00710383"),
    "ch_ad": ("Published source", "Companies House: Allied Dunbar Assurance plc (00865292)",
              "https://find-and-update.company-information.service.gov.uk/company/00865292"),
    "vdh2023": ("Published source", "Arjen van der Heide, Dealing in Uncertainty (Bristol University Press, 2023), "
                "chapter 3", "https://www.cambridge.org/core/books/dealing-in-uncertainty/"
                "shifting-boundaries-between-insurance-and-finance/358F5532AC6BB53FD7995A951D891746"),
    # Steve
    "steve_cert": ("Steve's analysis", "There are two certainties in life (LinkedIn article)",
                   ARTICLES["certainties"][1]),
    "steve_cert_exp": ("Steve's experience", "There are two certainties in life (LinkedIn article)",
                       ARTICLES["certainties"][1]),
    "steve_86": ("Steve's analysis", "86 days, 10 hours, 5 minutes and 42 seconds (LinkedIn article)",
                 ARTICLES["days86"][1]),
    "steve_86_exp": ("Steve's experience", "86 days, 10 hours, 5 minutes and 42 seconds (LinkedIn article)",
                     ARTICLES["days86"][1]),
})

if INCLUDE_EVIDENCE:
    SOURCES["q_nominees"] = ("Provider evidence",
                             "Quotations from Just (11 August 2026) and Canada Life (10 August 2026): evidence extract",
                             EVIDENCE_URL)

# ---------------------------------------------------------------------------
# Video data
# ---------------------------------------------------------------------------

# R02 (Clara, 3 October 2026): the exclusions and their condition, used word for word wherever the
# pensions page summarises them.
EXCLUSIONS_TEXT = (
    "The excluded categories are dependants' scheme pensions; trivial commutation lump sum death benefits "
    "replacing those pensions; dependants' or nominees' annuities bought together with the member's own "
    "lifetime annuity; and qualifying death in service benefits. The benefit must be payable only in one or "
    "more of those excluded forms. Having a choice of a non-excluded benefit can prevent the exclusion, even "
    "if an excluded form is chosen after death. Annuity guarantee payments and value protection need their "
    "own inheritance tax assessment."
)
EXCLUSIONS_SOURCES = ["ihta150A", "tn331", "tn332", "tn333", "tn334", "tn2_dsp"]

# R05 (Clara, 3 October 2026): the pension asset figure, carrying C05's distinction to the video page.
TRILLION_TEXT = (
    "The Pensions Policy Institute's DC Future Book 2025 reports UK defined contribution pension assets of "
    "£1.2 trillion in 2024. This shows the scale of the pension category affected, not the precise value "
    "newly taxable from April 2027 or the amount of tax to be collected. Being within the rules does not "
    "mean every pound is taxed."
)

VIDEOS = [
    {
        "slug": "pensions-and-inheritance-tax-from-april-2027",
        "id": "z5OJGXxvEF4",
        "number": 1,
        "title": "How will your pension be taxed when you die after April 2027?",
        "short_title": "Pensions and inheritance tax from April 2027",
        "seo_title": "How will your pension be taxed when you die after April 2027?",
        "seo_description": "From 6 April 2027 unused pensions come into inheritance tax. What changes, what is excluded, and how, in a severe case, £500,000 could cost £516,000.",
        "meta_description": (
            "From 6 April 2027, most unused pension funds and pension death benefits count as part of "
            "the estate for UK inheritance tax. What changes, which pensions are excluded, and how a £500,000 "
            "pension could cost a family £516,000 in tax. Video, key facts and full transcript "
            "by Steve Hunt ACII TEP."
        ),
        "published": "2026-09-29",
        "modified": "2026-10-03",
        "modified_without_guide": "2026-10-03",
        "as_at": "3 October 2026",
        "guide": ("pensions-and-inheritance-tax-from-april-2027/guide",
                  "Pensions and inheritance tax from April 2027: every question answered"),
        "published_iso": "2026-09-29T16:38:32+01:00",
        "seconds": 647,
        "duration_iso": "PT10M47S",
        "duration_text": "10 min 47 sec",
        "short_answer": [
            "From 6 April 2027, most unused pension funds and pension death benefits count as part of "
            "your estate for inheritance tax, and can be taxed at 40% on death. Pensions left to a "
            "spouse or civil partner are usually exempt, subject to the conditions of the spouse "
            "exemption. Unmarried partners are not covered.",
            EXCLUSIONS_TEXT,
            "If your estate with the pension is under the nil rate bands, there is no inheritance tax at "
            "all. In a severe case, with a large estate and a beneficiary who is a higher earner, a "
            "£500,000 pension could cost a family £516,000 in inheritance tax and income tax combined. "
            "The result depends on the stated assumptions and is not a typical pension tax rate.",
        ],
        "short_sources": ["ihta150A", "fa2026s71", "ihta18", "tn331", "tn332", "tn333", "tn334", "tn2_dsp",
                          "steve_example"],
        "chapters": [
            (0, "How will your pension be taxed after April 2027?"),
            (35, "What changes on 6 April 2027"),
            (67, "Worked example: £516,000 of tax on a £500,000 pension"),
            (138, "One word: \"notional\""),
            (207, "Which pensions are excluded"),
            (249, "How the £516,000 adds up"),
            (493, "No business or farm reliefs, and a six-month deadline"),
            (537, "The answer in three lines"),
            (611, "What's next, and Roy Jenkins"),
        ],
        "key_facts": [
            ("From 6 April 2027, most unused pension funds and pension death benefits count as part of the "
             "estate for inheritance tax: Inheritance Tax Act 1984, s.150A, inserted by Finance Act 2026, "
             "s.66, for deaths on or after 6 April 2027 (Finance Act 2026, s.71).",
             ["ihta150A", "fa2026s66", "fa2026s71", "tn"]),
            ("Pensions left to a spouse or civil partner are usually exempt, subject to the conditions in "
             "section 18 of the Inheritance Tax Act 1984. Unmarried partners are not covered.",
             ["ihta18", "tn34"]),
            (EXCLUSIONS_TEXT,
             EXCLUSIONS_SOURCES),
            ("The residence nil rate band reduces by £1 for every £2 that an estate is over £2 million "
             "(Inheritance Tax Act 1984, s.8D).",
             ["ihta8D", "rnrb"]),
            ("If death is at 75 or over, the person who inherits the pension also pays income tax on what "
             "they draw.",
             ["inherit"]),
            ("Business property relief, agricultural property relief and the ten-year instalment option do "
             "not apply to pension funds. The tax is due by the end of the sixth month after the month of "
             "death, with interest after that (Inheritance Tax Act 1984, ss.226 and 233).",
             ["ihta226", "ihta233", "tn1123", "tn1124", "payiht"]),
            (TRILLION_TEXT,
             ["ppi2025", "pa1trn"]),
            ("This is a severe, assumption-dependent illustration, not a typical pension tax rate. Other families "
             "may pay less or no tax.",
             ["steve_example"]),
        ],
        "assumptions": (
            "Assumptions in the worked example: Mr Miggins died under 75 and before 6 April 2027, leaving his "
            "pension to Mrs Miggins; she dies in 2029, aged over 75; her estate without the pension is "
            "£2 million; his unused nil rate band and residence nil rate band are both transferred in full and "
            "claimed; a home worth at least £350,000 passes to direct descendants; there are no other gifts, "
            "reliefs or deductions; the inheritance tax on the pension is paid straight from the pension, which "
            "is an option, not a rule; Amy earns £100,000 a year and draws £24,000 a year from the pension for "
            "15 years; 2026/27 rates and allowances, frozen; no fund growth; English income tax rates. This is "
            "a constant-rules illustration, not a forecast of future tax rates. Mr and Mrs Miggins are "
            "fictitious. The arithmetic is not."
        ),
        "faq": [
            ("What changes to pensions and inheritance tax on 6 April 2027?",
             "From 6 April 2027, unused pension money from personal pensions, SIPPs and money purchase "
             "company pension schemes becomes part of your estate for inheritance tax, and can be taxed at "
             "40% on your death. The change is made by section 150A of the Inheritance Tax Act 1984, "
             "inserted by section 66 of the Finance Act 2026, and it applies to deaths on or after 6 April "
             "2027. Spouse and civil partner exemptions still apply. Common law partners are not covered.",
             ["ihta150A", "fa2026s66", "fa2026s71", "ihta18", "tn"]),
            ("Which pensions are excluded from inheritance tax from April 2027?",
             EXCLUSIONS_TEXT,
             EXCLUSIONS_SOURCES),
            ("Can the combined family tax cost of a £500,000 pension be more than the pension itself?",
             "In a severe case, yes. In the worked example, Mrs Miggins inherited a £500,000 pension from "
             "her husband, who died before 75, so it could all have been paid out tax free. Because her own "
             "estate was already £2 million, adding the pension increased the inheritance tax on her estate "
             "by £300,000, an effective 60%. Because she died over 75, her daughter Amy then paid income tax "
             "on what she drew, also at an effective 60% because of the personal allowance taper, adding "
             "£216,000 over 15 years. Total extra tax across the family: £516,000, which is £16,000 more "
             "than the pension was worth. The £516,000 is not all taken out of the pension: the pension pays "
             "£140,000 of the inheritance tax, the rest of the estate pays the other £160,000 of the increase, "
             "and the £216,000 is income tax on Amy's withdrawals. The result depends on the assumptions "
             "listed with the example.",
             ["ihta150A", "ihta8D", "ihta265", "ita35", "itrates", "inherit", "steve_example"]),
            ("Why is the pension taxed at 60% in the example rather than 40%?",
             "The residence nil rate band is reduced by £1 for every £2 that an estate is over £2 million "
             "(Inheritance Tax Act 1984, s.8D). Adding a £500,000 pension to a £2 million estate takes away "
             "£250,000 of the residence nil rate band, which costs another £100,000 at 40%, on top of the "
             "£200,000 charged on the pension itself. That is an additional £300,000 of tax on the £500,000 "
             "pension, an effective rate of 60%. It assumes the full residence nil rate band of £350,000, "
             "including the band transferred from Mr Miggins, would otherwise have been available.",
             ["ihta8D", "rnrb", "steve_example"]),
            ("Does the pension fund pay the inheritance tax it causes?",
             "Not in the example. The tax on an estate is shared out in proportion to the value of each part "
             "(Inheritance Tax Act 1984, s.265), so the pension bears its proportionate share of the whole "
             "estate's bill, not the extra tax it triggers. In the example the pension is one fifth of a "
             "£2.5 million estate. The total tax is £700,000, so the pension's share is £140,000, leaving "
             "£360,000 in the pension, which Amy then draws as taxable income. Paying that share straight "
             "from the pension, under the Pensions Direct Payment Scheme, is an option that the example "
             "assumes is used, not a rule. The personal representatives are responsible for reporting and "
             "paying the tax, and a beneficiary who receives pension property becomes jointly liable for the "
             "tax on it.",
             ["ihta265", "tn22", "tn7", "steve_example"]),
            ("Can business property relief, agricultural property relief or the ten-year instalment option apply to pension funds?",
             "No. HMRC's technical note says that you are not treated as owning the pension's assets, and "
             "uses that sentence to refuse business property relief, agricultural property relief, loss on "
             "sale relief and the ten-year instalment option. The tax on the pension must be settled by the "
             "end of the sixth month after the month of death, with interest running after that.",
             ["tn1123", "tn1124", "tn1121", "ihta226", "ihta233", "payiht"]),
            ("How will your pension be taxed when you die after April 2027?",
             "Your pension fund will form part of your estate on death, unless it goes to a spouse or civil "
             "partner or is one of the excluded types. If your estate with the pension is under the nil rate "
             "bands, £325,000 plus up to £175,000 for a home passing to direct descendants, each, so up to "
             "£1 million for a married couple, it pays no inheritance tax at all. Above that, the rate is 40%, "
             "rising to an effective 60% where the residence nil rate band tapers away, plus income tax for "
             "the person who inherits if you die at 75 or over.",
             ["ihta150A", "ihta8D", "ihta8A", "ihtgov", "inherit"]),
        ],
        "articles": [
            ("husband", "The worked example, Mrs Miggins and her daughter Amy."),
            ("oneword", "The word \"notional\", and the one clause that takes a pension back out of the net."),
        ],
        "related": [("Next video", "nominees-annuity",
                     "Nominees' annuity: what is it, how does it work, and what's the catch?")],
        "legislation": "Inheritance Tax Act 1984, s.8D, s.18, s.150A(1) and (6), s.226 and s.265; s.150A was "
                       "inserted by Finance Act 2026, s.66, for deaths on or after 6 April 2027 (s.71). Income Tax "
                       "Act 2007, s.35.",
        "notes": [
            {"phrase": "an estimated £1 trillion",
             "kind": "Source note",
             "text": "The £1 trillion is an estimate of the defined contribution pension money that comes within "
                     "the scope of inheritance tax. Pensions Age reported on 23 October 2025 that UK defined "
                     "contribution pension assets had reached £1.2 trillion (Pensions Policy Institute, DC Future "
                     "Book). Coming within scope does not mean it will all be taxed.",
             "sources": ["pa1trn"]},
            {"phrase": "an estimated £1 trillion",
             "kind": "Source clarification",
             "id": "pension-assets-note",
             "date": FIX_DATE,
             "text": TRILLION_TEXT + " The guide answers this in full: [How much pension money comes within "
                     "inheritance tax?](/pensions-and-inheritance-tax-from-april-2027/guide/"
                     "#how-much-pension-money-comes-within-inheritance-tax)",
             "sources": ["ppi2025", "pa1trn"]},
            {"phrase": "dependants' pensions from a defined benefit scheme",
             "kind": "Clarification",
             "text": "The exclusion covers dependants' scheme pensions from any type of pension arrangement, not "
                     "only defined benefit schemes. A widow's pension from a final salary scheme is the common "
                     "example.",
             "sources": ["ihta150A", "tn331"]},
            {"phrase": "dependants' pensions from a defined benefit scheme",
             "kind": "Clarification",
             "date": FIX_DATE,
             "text": EXCLUSIONS_TEXT,
             "sources": EXCLUSIONS_SOURCES},
            {"phrase": "The pension does not pay the tax that it's responsible for.",
             "kind": "Clarification",
             "text": "In the example the pension's share of the tax is paid straight from the pension, under the "
                     "Pensions Direct Payment Scheme. That is an option, not a rule. The personal representatives "
                     "are responsible for reporting and paying the tax, and a beneficiary who receives pension "
                     "property becomes jointly liable for the tax on it.",
             "sources": ["ihta265", "tn22", "tn7"]},
            {"phrase": "joint life annuities, including nominees' annuities.",
             "kind": "Clarification",
             "date": FIX_DATE,
             "text": "The exclusions and their conditions are set out in the updated [key facts](#key-facts) "
                     "and the [note at 3:27](#t207). The pension-asset figure is explained in the "
                     "[source clarification at 0:00](#pension-assets-note).",
             "sources": []},
        ],
        "transcript_file": "v1_transcript.tsv",
        "keywords": ["pension inheritance tax 2027", "pensions and inheritance tax", "inheritance tax on pensions",
                     "unused pension funds", "residence nil rate band taper", "notional estate", "Finance Act 2026",
                     "Inheritance Tax Act 1984 section 150A"],
    },
    {
        "slug": "nominees-annuity",
        "id": "YkoXcpnujEA",
        "number": 2,
        "title": "Nominees' annuity: what is it, how does it work, and what's the catch?",
        "short_title": "The nominees' annuity",
        "seo_title": "What is a nominees' annuity, and what's the catch?",
        "seo_description": "A joint life annuity for a child or grandchild, bought with your own annuity and outside inheritance tax from April 2027. Real quotes, and the catches.",
        "meta_description": (
            "A nominees' annuity pays an income to someone the pension member nominates, such as an adult "
            "child, after the member dies. How the version bought in the member's lifetime works, with two "
            "real quotations, and the catches, including whether buying one is a gift. Video, key facts and "
            "full transcript by Steve Hunt ACII TEP."
        ),
        "published": "2026-09-29",
        "modified": "2026-10-03",
        "guide": ("nominees-annuity/guide", "The nominees' annuity: every question answered"),
        "published_iso": "2026-09-29T18:27:44+01:00",
        "seconds": 919,
        "duration_iso": "PT15M19S",
        "duration_text": "15 min 19 sec",
        "short_answer": [
            "A nominees' annuity is an annuity paid to a nominee of a pension member: someone the member "
            "nominates, such as an adult child or grandchild, who is not a dependant under the pension tax "
            "rules. This page is about the version bought in the member's lifetime, together with the "
            "member's own lifetime annuity, either as one joint life annuity or as a related separate "
            "contract. When the member dies, the income carries on to the nominee for the rest of their "
            "life. Nominees' annuities can also be bought after the member's death, but that is a different "
            "route, and not the one excluded from inheritance tax.",
            "Bought in the member's lifetime with the member's own annuity, it is excluded from the member's "
            "estate for inheritance tax from 6 April 2027. On a real quotation from August 2026, a £500,000 "
            "pension fund was offered a joint life annuity of £29,153.64 a year for a father of 75, with 100% "
            "continuation to his daughter of 45.",
            "The catches: this route can only be set up by the member, while alive; the quotations illustrated "
            "have no guarantee period and no value protection; the two insurers who quoted in August 2026 wanted the "
            "nominee to be aged 40 or over; the nominee's income is taxable when the member dies at 75 or over; "
            "and whether the purchase counts as a lifetime gift for inheritance tax is not settled.",
        ],
        "short_sources": ["fa2004p27AA", "fa2004p27A", "ihta150A", "itepa646B", "tn333", "ptm072200", "q_nominees",
                          "q_age40"],
        "chapters": [
            (0, "Today's question"),
            (24, "What is a nominees' annuity?"),
            (90, "The legal definition"),
            (165, "Why is it in the 2004 Act?"),
            (216, "How it works: two real quotations"),
            (366, "What's the catch?"),
            (440, "Is buying one a gift?"),
            (483, "Bill's example: how a PET could arise"),
            (622, "The hedge"),
            (711, "When both lives end early"),
            (772, "The answer in brief"),
            (879, "Next video, and Roy Jenkins"),
        ],
        "key_facts": [
            ("Legal definition: Finance Act 2004, Schedule 28, paragraph 27AA(1), inserted by the Finance Act "
             "2015, Schedule 4, paragraph 3(2). A nominee must not be a dependant under the pension tax rules: "
             "paragraph 27A, inserted by the Taxation of Pensions Act 2014, Schedule 2, paragraph 3.",
             ["fa2004p27AA", "fa2015", "fa2004p27A", "tpa2014"]),
            ("Bought together with the member's own lifetime annuity means related to it: one joint life "
             "contract, or a separate contract with the same or another insurer bought within 7 days before or "
             "after the member's annuity (paragraph 27AA(2); HMRC PTM072200).",
             ["fa2004p27AA", "ptm072200"]),
            ("From 6 April 2027, a nominees' annuity bought together with the member's own lifetime annuity is "
             "excluded from the estate for inheritance tax: Inheritance Tax Act 1984, s.150A(6)(c), inserted "
             "by Finance Act 2026, for deaths on or after 6 April 2027. Nominees' annuities bought after the "
             "member's death are also allowed, but that is not the route that qualifies for this exclusion.",
             ["ihta150A", "fa2026s66", "fa2026s71", "tn333"]),
            ("Remaining guarantee payments and value protection death benefits come within inheritance tax "
             "from 6 April 2027. The example in the video leaves both out.",
             ["ihta150A"]),
            ("The quotations: Just, 11 August 2026, 5.83%, £29,153.64 a year. Canada Life, 10 August 2026, "
             "5.79%, £28,925.76 a year. Both on £500,000, parent 75, nominee 45, level, no guarantee, no value "
             "protection, monthly in arrears, 100% continuation, standard rates, no adviser charge. Naming the "
             "insurers records where the quotations came from. It is not a recommendation.",
             ["q_nominees"]),
            ("Age 40 or over, including age 40, is a provider condition (Just and Canada Life, August 2026), "
             "not a legal minimum. The other insurers asked in August 2026 said no at that time, though some "
             "were reviewing. The market may have changed since.",
             ["q_age40", "fa2004p27AA"]),
            ("Whether buying one is a gift for inheritance tax is not settled. That it may be is Steve's "
             "analysis, not HMRC's published position. The £50,000 in Bill's example is an assumed value for "
             "illustration: halving the income does not by itself set the tax value. The £20,000 assumes death "
             "within 3 years and no nil rate band or exemptions available. Taper relief reduces the tax after "
             "3 years.",
             ["ihta3A", "ihta7", "tn1125", "steve_pet"]),
            ("Whole of life cover continues beyond 7 years, and term cover protects only for its term. Premiums "
             "must be maintained and claim conditions met, and total premiums can exceed the payout.",
             []),
            ("In this example the annuity income is taxable, because Mr Miggins is 75 or over when he dies. If "
             "the member dies under 75, a nominees' annuity bought together with the member's own annuity is "
             "paid free of income tax (Income Tax (Earnings and Pensions) Act 2003, s.646B(3)). Salary sacrifice "
             "means Amy gives up salary in return for employer pension contributions; the annuity itself stays "
             "taxable, and any saving depends on her circumstances and pension limits. From 6 April 2029, the "
             "National Insurance exemption is limited to £2,000 a year of pension salary sacrifice.",
             ["itepa646B", "ptm072210", "nics2026"]),
            ("A level income loses buying power with inflation, and the purchase normally cannot be reversed "
             "after the cancellation period.",
             []),
        ],
        "assumptions": (
            "Mr Miggins, his brother Bill, and Amy are fictitious. The quotations are real, obtained in "
            "August 2026 for a LinkedIn article. Their guarantees have expired; they are not current offers. "
            "The original quotations and the insurers' answers are held on file. No client information is used."
        ),
        "faq": [
            ("What is a nominees' annuity?",
             "A nominees' annuity is an annuity paid to a nominee of a pension member: an individual nominated "
             "by the member, or by the scheme administrator, who is not a dependant under the pension tax rules, "
             "often an adult child or grandchild. The version on this page is bought in the member's lifetime "
             "together with the member's own lifetime annuity, so that when the member dies the income carries "
             "on to the nominee for the rest of their life. Nominees' annuities can also be bought after the "
             "member's death, but that is a different route, and not the one excluded from inheritance tax. The "
             "nominees' annuity came in with George Osborne's 2015 pension freedoms and has been possible since "
             "6 April 2015, but insurers have only recently started to write the lifetime version.",
             ["fa2004p27AA", "fa2004p27A", "fa2015", "ihta150A", "q_age40"]),
            ("What is the legal definition of a nominees' annuity?",
             "Finance Act 2004, Schedule 28, paragraph 27AA(1), inserted by the Finance Act 2015. An annuity "
             "payable to a nominee is a nominees' annuity if either it is purchased together with a lifetime "
             "annuity payable to the member, and the member becomes entitled to that lifetime annuity on or "
             "after 6 April 2015; or it is purchased after the member's death, the member dies on or after "
             "3 December 2014, and the nominee becomes entitled to the annuity on or after 6 April 2015. Under "
             "paragraph 27AA(2), it is purchased together with the member's lifetime annuity if it is related "
             "to it. Only the first route, bought together with the member's own annuity, is excluded from "
             "inheritance tax under section 150A(6)(c) of the Inheritance Tax Act 1984. A nominee is defined in "
             "paragraph 27A, inserted by the Taxation of Pensions Act 2014, and must not be a dependant.",
             ["fa2004p27AA", "fa2015", "fa2004p27A", "tpa2014", "ihta150A"]),
            ("Why is the nominees' annuity in the Finance Act 2004 if it came from the 2015 pension freedoms?",
             "Because the Finance Act 2015 inserted the new wording into the Finance Act 2004, which is the "
             "Act that holds the pension tax rules. So it appears in the 2004 Act, but it did not exist until "
             "the 2015 Act put it there. The definition of a nominee, in paragraph 27A, had been inserted a few "
             "months earlier by the Taxation of Pensions Act 2014.",
             ["fa2015", "tpa2014", "fa2004p27AA"]),
            ("How does a nominees' annuity work in practice?",
             "Take a father of 75 with a £500,000 pension fund and a daughter of 45. On real quotations from "
             "August 2026, Just offered £29,153.64 a year (£2,429.47 a month) at 5.83%, and Canada Life "
             "£28,925.76 a year at 5.79%. Both were level, with no guarantee period, no value protection, "
             "paid monthly in arrears, with 100% continuation to the daughter for the rest of her life. When "
             "the father dies, the same monthly income carries on to her. Bought together with his own "
             "annuity, it is excluded from his estate for inheritance tax from 6 April 2027. These are dated "
             "examples, not recommendations or current offers. A fresh quotation could give a different rate.",
             ["q_nominees", "ihta150A", "tn333"]),
            ("What is the catch with a nominees' annuity?",
             "The version excluded from inheritance tax can only be set up by the pension member, while alive, "
             "because it must be purchased together with a lifetime annuity payable to the member. So the "
             "opportunity to arrange this lifetime-purchased related annuity ends when the member dies. A widow "
             "who inherits her husband's pension cannot use that inherited pension to buy one, although she can "
             "use her own pension. The quotations illustrated have no guarantee period or value protection. "
             "Having neither is not a condition of the survivor-annuity exclusion; any such additional benefits "
             "need their own inheritance tax assessment. The insurers who quoted in August 2026 wanted the "
             "nominee to be aged 40 or over, which is a provider condition rather than a legal one. If the "
             "member dies at 75 or over, the nominee pays income tax on the income. And whether buying one is a "
             "lifetime gift for inheritance tax has not been settled.",
             ["fa2004p27AA", "ihta150A", "tn333", "itepa646B", "q_age40"]),
            ("Is buying a nominees' annuity a gift for inheritance tax?",
             "Nobody has settled it. What follows is Steve's analysis, not HMRC's published position. The "
             "argument: if a £100,000 pot would buy a single life annuity of £10,000 a year, and the member "
             "takes £5,000 a year instead so that 100% continues to his son, he has given up half his pension "
             "income. Applying the same proportion to the pot is one way to illustrate a value, £50,000; it is "
             "not the statutory valuation method, and the real figure would depend on the facts. If the "
             "purchase met the conditions for a potentially exempt transfer: nothing to pay if he lives seven "
             "years, and if "
             "he dies within seven years, up to £20,000 of tax at 40% on that illustrative figure in the worst "
             "case, with no nil rate band or exemptions available. Steve's reading of the law as written: buy "
             "one before 6 April 2027 and it may be a gift; buy one after 6 April 2027 out of a pension trust "
             "and it may not be a gift at all. Read alongside it HMRC's technical note, which says in its "
             "section on lifetime transfers that the pension changes 'do not alter the existing position for "
             "lifetime transfers'. The full argument is in his article Osborne's Get Out of Jail Card Under "
             "Attack.",
             ["ihta3A", "ihta7", "tn1125", "steve_pet"]),
            ("How can the seven-year gift risk be covered?",
             "One way is life assurance on the member's life, written in trust. A whole of life plan pays out "
             "whenever death happens, so it would pay if the gift failed through death within seven years; "
             "seven-year term cover would protect only that period. There is one more risk, both lives ending "
             "early. If the nominee were to die soon after the member, the continuation ends with them, so the "
             "nominee could take out a term policy on their own life, in trust, which protects only for its "
             "term, for example ten years. Premiums must be kept up and claim conditions met, and total "
             "premiums can exceed the payout. Whether any of this is worth doing depends on the person's "
             "circumstances.",
             []),
            ("Is the income from a nominees' annuity taxable?",
             "It depends on the member's age at death and the applicable conditions. In this example, Mr "
             "Miggins is already 75, so Amy's annuity income is taxable. Where the member dies under 75, a "
             "qualifying related nominees' annuity can instead be paid free of income tax. A nominee who pays "
             "tax on the income and is employed may be able to get some or all of that tax back by paying more "
             "into their own pension through salary sacrifice, but the annuity itself stays taxable, and any "
             "saving depends on their circumstances and pension limits. From 6 April 2029, the National "
             "Insurance exemption is limited to £2,000 a year of pension salary sacrifice.",
             ["itepa646B", "ptm072210", "nics2026"]),
        ],
        "articles": [
            ("oneword", "The Mr Miggins and Amy nominees' annuity figures."),
            ("jail", "Is buying one a gift? The full detail."),
            ("killed", "Background: where the nominees' annuity came from."),
        ],
        "related": [("Previous video", "pensions-and-inheritance-tax-from-april-2027",
                     "How will your pension be taxed when you die after April 2027?"),
                    ("Next video", "whole-of-life-assurance",
                     "Whole of life assurance: what is it, why does a whole generation distrust it, and what has changed?")],
        "legislation": "Finance Act 2004, Schedule 28, paragraph 27A (inserted by the Taxation of Pensions Act 2014, "
                       "Schedule 2, paragraph 3) and paragraph 27AA (inserted by the Finance Act 2015, Schedule 4, "
                       "paragraph 3(2)); Income Tax (Earnings and Pensions) Act 2003, s.646B(3); Inheritance Tax Act "
                       "1984, s.3A, s.7(4) and s.150A(6)(c), the last inserted by Finance Act 2026, s.66.",
        "notes": [
            {"phrase": "A nominees' annuity is a joint life annuity",
             "kind": "Clarification",
             "text": "This describes the version bought in the member's lifetime with the member's own annuity, "
                     "which is the one this video is about. In law a nominees' annuity is an annuity paid to a "
                     "nominee who is not a dependant of the member, and it can also be bought after the member's "
                     "death, but that route is not excluded from inheritance tax.",
             "sources": ["fa2004p27AA", "fa2004p27A", "ihta150A"]},
            {"phrase": "currently needs to be over the age of 40.",
             "kind": "Correction",
             "text": "The insurers' rule is age 40 or over. As the video goes on to say, they would not accept a "
                     "nominee under 40. This was a provider condition in August 2026, not the law.",
             "sources": ["q_age40"]},
            {"phrase": "The rest of the market is, at the time of writing,",
             "kind": "Note",
             "text": "At the time of writing means August 2026, when the insurers were asked. The market may have "
                     "changed since.",
             "sources": ["q_age40"]},
            {"phrase": "as one joint life annuity.",
             "kind": "Clarification",
             "text": "It can be one joint life contract, or a separate contract with the same or another insurer "
                     "bought within 7 days before or after the member's own annuity. Either way it counts as "
                     "related, which is what purchased together means in the law.",
             "sources": ["fa2004p27AA", "ptm072200"]},
            {"phrase": "The nominees' annuity option dies with the member.",
             "kind": "Clarification",
             "text": "This means the opportunity to arrange this lifetime-purchased, related nominees' annuity, the "
                     "route that is excluded from inheritance tax, ends when the member dies. Nominees' annuities "
                     "can also be bought after the member's death, but that route is not excluded. The widow in the "
                     "example cannot use her inherited pension to buy one, but she can use her own pension.",
             "sources": ["fa2004p27AA", "ihta150A"]},
            {"phrase": "The income to Amy is taxable, yes,",
             "kind": "Clarification",
             "text": "Taxable in this example because Mr Miggins is 75. If the member dies under 75, a nominees' "
                     "annuity bought together with the member's own annuity is paid free of income tax.",
             "sources": ["itepa646B", "ptm072210"]},
        ],
        "transcript_file": "v2_transcript.tsv",
        "keywords": ["nominees' annuity", "nominee annuity", "joint life annuity", "pension inheritance tax 2027",
                     "potentially exempt transfer", "whole of life assurance", "Finance Act 2004 Schedule 28",
                     "paragraph 27AA"],
    },
    {
        "slug": "whole-of-life-assurance",
        "id": "gA2AwqiSg2I",
        "number": 3,
        "title": "Whole of life assurance: what is it, why does a whole generation distrust it, and what has changed?",
        "short_title": "Whole of life assurance",
        "seo_title": "Whole of life assurance: what is it, and what has changed?",
        "seo_description": "Whole of life assurance pays out whenever death occurs, if the premiums are paid. Why a generation distrusts it, and what has changed since the 1980s.",
        "meta_description": (
            "Whole of life assurance pays a fixed sum when you die, whenever that is, provided the premiums are "
            "paid. What it is, why the unit-linked plans of the 1980s made a generation distrust it, and what "
            "has changed: guaranteed premiums, and a real quotation showing how it can be used for "
            "generational wealth transfer. Video, key facts and full transcript by Steve Hunt ACII TEP."
        ),
        "published": "2026-10-01",
        "modified": WOL_GUIDE_RELEASE,
        "modified_without_guide": "2026-10-03",
        "guide": (WOL_GUIDE_SLUG, "Whole of life assurance: every question answered"),
        "published_iso": "2026-10-01T07:06:59+01:00",
        "seconds": 783,
        "duration_iso": "PT13M3S",
        "duration_text": "13 min 3 sec",
        "short_answer": [
            "Whole of life assurance puts a monetary value on a person's life, the sum assured, and pays it out "
            "when that person dies, whenever that is, provided the premiums are paid. Under the Life Assurance "
            "Act 1774 you can only insure a life in which you have an insurable interest. An individual has an "
            "unlimited insurable interest in their own life and in the life of their spouse or civil partner.",
            "In Steve's experience, a generation distrusts it because of the unit-linked whole of life plans of "
            "the 1980s, sold by the hundreds of thousands by companies like Abbey Life and Allied Dunbar: "
            "reviewable premiums, cover that could be cut, policies that lapsed with nothing to show for years "
            "of premiums, and payouts that sometimes fell short of the premiums paid in.",
            "What has changed: a conventional whole of life policy with guaranteed, non-reviewable premiums is "
            "whole of life again, with the premium fixed from day one. Reviewable policies also exist. On a real "
            "quotation, a man of 75 pays £1,555.20 a month for £500,000 written in trust. Die at 80 and the "
            "trust receives £500,000 for £93,312 of premiums. The same £93,312 left in his estate would leave "
            "his family £55,987 after 40% inheritance tax, or as little as £37,325 at an effective 60%, "
            "ignoring investment returns and inflation. In this quotation, total premiums only pass the sum "
            "assured if he lives to nearly 102. The catch is that age and health decide the premium, and "
            "whether cover is offered at all.",
        ],
        "short_sources": ["laa1774", "cpa253", "mg", "fos", "ihta8D", "q_wol", "steve_history"],
        "chapters": [
            (0, "Today's question"),
            (26, "What is whole of life assurance?"),
            (57, "Before 1774: life assurance as gambling"),
            (86, "Insurable interest and the 1774 Act"),
            (145, "Why does a whole generation distrust it?"),
            (179, "The unit-linked companies"),
            (267, "The wild west before 1988"),
            (323, "What has changed?"),
            (346, "Generational wealth transfer: Mr Miggins at 75"),
            (441, "Keep the money instead: 40% or 60%"),
            (553, "Car insurance, term insurance, whole of life"),
            (624, "The answer in three lines"),
            (644, "The two whens: age and health"),
            (701, "James Dodson and the Amicable Society"),
            (737, "What's next, and Roy Jenkins"),
        ],
        "key_facts": [
            ("Whole of life assurance puts a monetary value on a life, the sum assured, and pays it when that "
             "person dies, whenever that is, provided the premiums are paid. On a conventional guaranteed-premium "
             "plan the premium is fixed from day one and is never reviewed. Reviewable whole of life policies "
             "also exist, and on those the premium or the cover can change at a review.",
             ["fos"]),
            ("Life Assurance Act 1774, also known as the Gambling Act: a policy on someone's life is void unless "
             "the person taking it out has an insurable interest in that life (section 1), and the amount "
             "recoverable is limited to the value of that interest (section 3). An individual has an unlimited "
             "insurable interest in their own life and in the life of their spouse, and civil partners have one "
             "in each other by statute (Civil Partnership Act 2004, s.253). Beyond that the only limits are the "
             "insurer accepting the risk and the premiums being affordable.",
             ["laa1774", "cpa253", "mg"]),
            ("In Steve's experience, the unit-linked whole of life plans of the 1980s were investment policies "
             "with a death benefit attached. Premiums were reviewable: to keep the same cover the premium could "
             "go up, or the cover could be cut, and some policies lapsed with nothing to show for years of "
             "premiums. The new rules on selling investments came in under the Financial Services Act 1986, "
             "with the main provisions in force from 29 April 1988.",
             ["fsa1986", "si1988", "fos", "steve_history"]),
            ("The quotation in the video: a man of 75, £500,000 of conventional whole of life assurance with "
             "guaranteed premiums, written in trust, premium £1,555.20 a month, £18,662.40 a year.",
             ["q_wol"]),
            ("Premiums paid against the £500,000 paid to the trust: death at 80, £93,312; at 85, £186,624; at 90, "
             "£279,936; at 95, £373,248; at 100, £466,560. In this quotation, total premiums pass the sum assured "
             "only after about 26 years and 10 months, when he would be nearly 102. A different age or premium "
             "gives a different answer, and total premiums can exceed the payout.",
             ["q_wol"]),
            ("Keep that money in the estate instead and the £93,312 he would have paid by 80 is taxed at 40%, "
             "leaving £55,987. Where it falls within the residence nil rate band taper, because the estate is "
             "over £2 million and enough residence nil rate band is still there to be lost, the band is reduced "
             "by £1 for every £2 over (Inheritance Tax Act 1984, s.8D), an effective 60%, leaving £37,325. These "
             "figures ignore investment returns and inflation.",
             ["ihta8D", "rnrb"]),
            ("Written in trust, the sum assured is paid to the trustees and does not form part of the estate. "
             "Premiums paid for a policy held in trust are gifts, exempt only where an exemption applies. The "
             "£3,000 annual exemption (s.19) covers only £3,000 a year, far less than this £18,662.40 premium. "
             "Normal expenditure out of income (s.21) applies only if the payments are part of the person's "
             "normal expenditure, are made out of income, and leave enough income to keep their usual standard "
             "of living, and section 21 has a special rule where an annuity has been bought on the same life. "
             "The example assumes the premiums qualify in full, which has to be shown on the facts.",
             ["ihta19", "ihta21"]),
            ("Term insurance, like car or house insurance, is a cost if it does not pay out. Whole of life "
             "assurance pays out on an event that is certain to happen, provided the premiums are kept up; the "
             "only unknown is when. That does not mean the premiums are refunded. The premiums must be paid for "
             "life: stop the premiums and the cover stops.",
             []),
            ("Age and health decide the premium, and whether cover is offered at all, and neither stays still. "
             "Cover available today may not be available after a scan or a blood test tomorrow.",
             []),
            ("James Dodson, who worked out the level premium system still used to price whole of life assurance, "
             "was refused admission by the Amicable Society, which admitted no one over 45. He died in 1757, "
             "before the Equitable Society he had planned opened in 1762, leaving three children unprovided for.",
             ["dnb", "actuary"]),
        ],
        "assumptions": (
            "Mr Miggins is fictitious. The quotation is real, obtained in 2026 and held on file; premiums depend "
            "on age, health and the insurer, and could differ on the day. The comparisons use the amounts as "
            "paid, with no investment returns or inflation, and assume the premiums are exempt gifts in full. "
            "The 60% figure assumes the extra money falls entirely within the residence nil rate band taper: "
            "the estate is over £2 million and enough residence nil rate band, up to £350,000 with a full "
            "transferred band, is still there to be lost. The whole band has gone once an estate reaches "
            "£2.7 million. Figures are rounded to the pound."
        ),
        "faq": [
            ("What is whole of life assurance?",
             "Whole of life assurance puts a monetary value on a person's life, for example £500,000, which is "
             "called the sum assured. When that person dies, the insurance company pays the sum assured, "
             "whenever death occurs, provided the premiums have been paid. In its basic, traditional form it "
             "is as simple as that, and it has worked that way since the Life Assurance Act 1774.",
             ["laa1774"]),
            ("What is insurable interest?",
             "Before 1774 it was common for the rich to take out life assurance on complete strangers, and even "
             "on kings and queens, in the coffee houses of London. It was a form of gambling: the preamble to the "
             "Life Assurance Act 1774, also known as the Gambling Act, says such insurances had introduced 'a "
             "mischievous kind of gaming'. The Act says you cannot take out a life assurance policy on someone "
             "unless you have an insurable interest in that person, meaning you would suffer a financial loss if "
             "they died. An individual has an unlimited insurable interest in their own life and in the life of "
             "their spouse or civil partner, so a husband could insure his wife for £10 million or £100 million. "
             "The only limits are an insurer accepting the risk and the premiums being paid.",
             ["laa1774", "cpa253", "mg"]),
            ("Why does a whole generation distrust whole of life assurance?",
             "This is Steve's account, from working in the industry since 1980. For 200 years whole of life "
             "assurance did exactly what it was designed to do: pay a lump sum on death, often used to cover "
             "death duties. Then the unit-linked companies of the 1960s to 1980s, Abbey Life, Hambro Life and "
             "later Allied Dunbar among them, brought in the unit-linked whole of life policy, an investment with "
             "a death benefit attached. Premiums could be reviewed, cover could be cut, some policies lapsed with "
             "nothing to show for years of premiums, and on death the sum assured sometimes fell short of the "
             "premiums paid in. They were sold by the hundreds of thousands in the wild west before the new rules "
             "on selling investments arrived in 1988. Boomers watched the foot-in-the-door salesman and the "
             "mis-selling in real time, and many vowed never to be caught again.",
             ["steve_history", "fos", "fsa1986", "si1988"]),
            ("What has changed with whole of life assurance?",
             "Today, a conventional whole of life policy with guaranteed, non-reviewable premiums is whole of life "
             "again: a premium fixed from day one, and a payout whenever death occurs, provided the premiums are "
             "paid. That type of policy has no premium reviews and the cover is not cut. Reviewable whole of life "
             "policies also exist, so the type matters. That is why a guaranteed-premium policy can be used for "
             "generational wealth transfer. Using it that way does not make it an investment: it is an insurance "
             "contract that pays the sum assured on death, subject to its terms.",
             ["fos", "q_wol"]),
            ("How can whole of life assurance be used for generational wealth transfer?",
             "Take a real quotation for a man of 75: £500,000 of whole of life assurance with guaranteed premiums, "
             "written in trust, at £1,555.20 a month, £18,662.40 a year. If he dies at 80 he has paid £93,312 in "
             "premiums and the trust receives £500,000. At 85, £186,624 paid, £500,000 received. At 90, £279,936. "
             "At 95, £373,248. At 100, £466,560. In every case the trust receives £500,000. In this quotation, "
             "total premiums pass the sum assured only if he lives to nearly 102, after about 26 years and "
             "10 months of premiums. The premiums he pays today buy £500,000 for the next generation, provided "
             "they are kept up, and if he dies young the trust gets considerably more than he paid in. If he "
             "lives long enough, he pays in more than the trust receives.",
             ["q_wol"]),
            ("What happens if the premium money stays in the estate instead?",
             "Left in his estate, the money is taxed at 40% inheritance tax, or an effective 60% where it falls "
             "within the residence nil rate band taper, which needs an estate over £2 million with enough "
             "residence nil rate band still there to be lost. Die at 80 and the £93,312 he would have paid in "
             "premiums leaves his family £55,987 after 40% tax, or as little as £37,325 at 60%. Use the same "
             "money for premiums on a whole of life plan in trust and, if he dies at 80, the family trust "
             "receives £500,000. This compares the amounts as paid, ignoring investment returns and inflation, "
             "and assumes the premiums are exempt gifts.",
             ["ihta8D", "rnrb", "ihta21", "q_wol"]),
            ("Is whole of life assurance just a cost, like car insurance?",
             "Not in the same way. Car insurance, house insurance and term insurance are a cost if they do not "
             "pay out, and most people with term insurance do not die during the term. Whole of life assurance "
             "pays out on an event that is certain to happen, provided the premiums are kept up, so the policy "
             "will pay its sum assured. That does not mean the premiums are refunded. In the particular age-75 "
             "quotation used here, total premiums would exceed the £500,000 sum assured only after about 26 years "
             "and 10 months. Different premiums and starting ages produce different results, and total premiums "
             "can exceed the payout. The premiums must be paid for life, though: stop the premiums and the cover "
             "stops.",
             ["q_wol"]),
            ("Can anyone get whole of life assurance?",
             "No. There are two whens: when the insurer will pay out if you have a policy, and how long cover "
             "will remain available to you. To get whole of life assurance the insurer looks at your age and "
             "your health, decides the premium, and decides whether to offer cover at all. Neither age nor "
             "health stands still, and a future scan that is not clear, or a blood test that needs follow-up, "
             "could mean this type of cover is no longer available.",
             []),
            ("Who was James Dodson?",
             "James Dodson was the mathematician who worked out the level premium system, the way whole of "
             "life assurance is still priced today. He was refused admission by the Amicable Society, which "
             "admitted no one over 45, and he died in 1757, before the Equitable Society he had planned opened "
             "its doors in 1762, leaving three children unprovided for. Steve has written about him, and the "
             "pastor whose mortality tables started it all, in his LinkedIn article The Pastor Who Tried to "
             "Prove God and Accidentally Predicted Death.",
             ["dnb", "actuary"]),
        ],
        "articles": [
            ("certainties", "How whole of life was hijacked in the 1980s, and Certainty³: guaranteed income funding guaranteed premiums."),
            ("days86", "The history: Abbey Life, Hambro Life and the first era of mis-selling."),
            ("pastor", "James Dodson, the Amicable Society and the level premium."),
        ],
        "related": [("Previous video", "nominees-annuity",
                     "Nominees' annuity: what is it, how does it work, and what's the catch?")],
        "legislation": "Life Assurance Act 1774, ss.1 to 3; Civil Partnership Act 2004, s.253; Inheritance Tax Act "
                       "1984, s.8D, s.19 and s.21; Financial Services Act 1986, since repealed.",
        "notes": [
            {"phrase": "Today, whole of life assurance is whole of life again:",
             "kind": "Clarification",
             "text": "This describes conventional whole of life policies with guaranteed, non-reviewable premiums, "
                     "the type in this video. Reviewable whole of life policies also exist, and on those the "
                     "premium or the cover can change at a review.",
             "sources": ["fos"]},
            {"phrase": "then the net amount to the family could be as little as £37,325.",
             "kind": "Clarification",
             "text": "The 60% case assumes the extra money falls entirely within the residence nil rate band "
                     "taper, with enough of the band, including a full transferred band, still there to be lost. "
                     "These comparisons use the amounts as paid and ignore investment returns and inflation.",
             "sources": ["ihta8D", "rnrb"]},
            {"phrase": "The premiums are not lost.",
             "kind": "Clarification",
             "text": "This means the policy pays its sum assured on death, whenever that is, provided the premiums "
                     "have been kept up. It does not mean the premiums are refunded. In this quotation, total "
                     "premiums would pass the £500,000 sum assured after about 26 years and 10 months, and total "
                     "premiums can exceed the payout.",
             "sources": ["q_wol"]},
        ],
        "transcript_file": "v3_transcript.tsv",
        "keywords": ["whole of life assurance", "whole of life insurance", "whole of life policy",
                     "generational wealth transfer", "life assurance in trust", "unit-linked whole of life",
                     "Life Assurance Act 1774", "insurable interest", "guaranteed premiums", "inheritance tax"],
    },
]

# Drop links to guides that are not in this build (drafts), and keep those pages' dates as they were.
_LIVE_GUIDE_SLUGS = {g["slug"] for g in GUIDES}
for _v in VIDEOS:
    if _v.get("guide") and _v["guide"][0] not in _LIVE_GUIDE_SLUGS:
        del _v["guide"]
        if "modified_without_guide" in _v:
            _v["modified"] = _v["modified_without_guide"]

# What changed on each page at the 1 October 2026 review, shown on the corrections page.
CORRECTIONS_LOG = [
    ("3 October 2026", "A new evidence page was published, and the nominees' pages now link to it. No answers "
                       "changed.", [
        ("nominees-annuity/quotations", [
            "Published: an evidence extract for the two nominees' annuity quotations used on this site. It sets out "
            "the figures and terms each insurer quoted, what each was asked for, how long the second life's income "
            "lasts and what was withheld. The quotations have expired and are not current offers.",
        ]),
        ("nominees-annuity", [
            "The Provider evidence source for the two quotations now links to the evidence page, in the source "
            "lists and the structured data. Nothing else changed.",
        ]),
        ("nominees-annuity/guide", [
            "The Provider evidence source for the two quotations now links to the evidence page, in the source "
            "lists and the structured data. No answers changed.",
        ]),
    ]),
    ("3 October 2026", "Further corrections: fixed the sources page's original publication date at 1 October "
                       "2026; aligned the pensions video-page and description summaries with the guide's "
                       "exclusion conditions, spouse-exemption conditions and worked-example assumptions; "
                       "clarified the pension-asset estimate and dated quotation wording; retained the nominees' "
                       "guide's contractual and lifetime-transfer qualifications in the shorter video-page "
                       "answers; and added the nominees' guide link to the video's description. The guides' "
                       "existing answers and the recorded transcript text were not changed. New dated transcript "
                       "annotations identify the clarifications. In the same release, the pensions page and its "
                       "video description now describe the worked example as a severe, assumption-dependent "
                       "illustration rather than saying most families will pay far less; the home page "
                       "introduction and the pensions page description no longer say pensions come into "
                       "inheritance tax for the first time; and the nominees' video description now says when "
                       "the annuity income is taxable.", []),
    ("3 October 2026", "Two new pages were published, and the existing pages gained links to them. No answers on "
                       "the existing pages were changed.", [
        ("pensions-and-inheritance-tax-from-april-2027/guide", [
            "Published: Pensions and inheritance tax from April 2027: every question answered. A guide of 28 "
            "questions drawn from Steve's LinkedIn articles and the video, each answer with its sources, checked "
            "against the Finance Act 2026, the information regulations made in July 2026 (SI 2026/818) and HMRC's "
            "technical notes of May and August 2026.",
        ]),
        ("pensions-and-inheritance-tax-from-april-2027", [
            "Guide links were added near the top, below the questions and under the related articles. Apart from "
            "the site-wide navigation and author updates listed below, the existing answers and transcript were "
            "unchanged.",
        ]),
        ("nominees-annuity", [
            "The guide link was also added near the top, after the short answer. Apart from the site-wide "
            "navigation and author updates listed below, the existing answers and transcript were unchanged.",
        ]),
        ("nominees-annuity/guide", [
            "The introduction now also gives the question in everyday terms: whether a pension annuity can keep "
            "paying a son, daughter or grandchild after the parent dies. The page's HTML title is now "
            "'Nominees' annuity: UK rules and inheritance tax from 2027'. No answers changed.",
        ]),
        ("", [
            "An About page was added, linked from the menu, the footer and the author box on every page.",
        ]),
    ]),
    ("2 October 2026", "A new page was published. Later the same day, after a further review, the published page "
                       "was corrected. The corrections are listed below. No answers on the video pages were changed.", [
        ("nominees-annuity/guide", [
            "Published: The nominees' annuity: every question answered. A guide of 25 questions drawn from Steve's "
            "four LinkedIn articles on the subject and the video, each answer with its sources. Steve's reading of the "
            "gift question is labelled as his analysis, with HMRC's published position beside it.",
            "Corrected the same day: the answer to 'Who can be a nominee?' used to say that a scheme administrator "
            "can only nominate where the member has left no dependant and made no nomination of their own. It now "
            "follows the Act: a scheme administrator's nomination only counts while there is no dependant and no "
            "individual or charity nominated by the member for the relevant benefits (Finance Act 2004, Sch. 28, "
            "para. 27A(2)).",
            "Corrected the same day: the answer to 'How can the seven-year risk be covered?' used to begin 'Life "
            "assurance can provide money following a covered death.' It now says that the relevant cover is on the "
            "member's life, and that a policy held in a suitable trust can provide money to the trustees outside the "
            "member's estate. Sections 263 and 268 of the Inheritance Tax Act 1984 and HMRC's manual at IHTM20211 "
            "were added to its sources.",
            "Corrected the same day: the Supreme Court judgment in HMRC v Parry was labelled Law and is now labelled "
            "Case law, and the worked example behind the £516,000 figure is now linked from the answer that uses it.",
        ]),
        ("nominees-annuity", [
            "A link to the full guide was added below the questions. Nothing else changed.",
        ]),
    ]),
    ("1 October 2026", "All three video pages were reviewed against the law and HMRC's published guidance. These are the changes.", [
        ("nominees-annuity", [
            "The answer to 'Is the income from a nominees' annuity taxable?' used to begin 'Yes'. It now explains "
            "that the income is taxable where the member dies at 75 or over, as in the example, and can be paid "
            "free of income tax where the member dies under 75 (Income Tax (Earnings and Pensions) Act 2003, "
            "s.646B(3)).",
            "The page now makes clear that it is about the nominees' annuity bought in the member's lifetime, which "
            "is the version excluded from inheritance tax, and that nominees' annuities can also be bought after "
            "the member's death by a different route. It also explains that the related annuity can be a separate "
            "contract bought within 7 days of the member's own annuity.",
            "Paragraph 27A of Schedule 28 to the Finance Act 2004, which defines a nominee, was said to have been "
            "inserted by the Finance Act 2015. It was inserted by the Taxation of Pensions Act 2014. The Finance "
            "Act 2015 inserted paragraph 27AA.",
            "The question whether buying one is a gift is labelled as Steve's analysis, with HMRC's technical note "
            "quoted alongside, and the £50,000 figure is described as an illustration, not the statutory valuation.",
            "The nominee's minimum age is stated as 40 or over throughout, tied to the insurers' answers in August "
            "2026.",
            "Dated notes were added to the transcript on the definition, the nominee's age, the separate-contract "
            "route, the after-death route and income tax.",
        ]),
        ("pensions-and-inheritance-tax-from-april-2027", [
            "The worked example now lists all of its assumptions, including the transferred nil rate bands, the "
            "home passing to direct descendants, and Amy drawing £24,000 a year for 15 years.",
            "The question 'Can inheritance tax on a £500,000 pension really cost more than the pension itself?' is "
            "now 'Can the combined family tax cost of a £500,000 pension be more than the pension itself?', because "
            "the £516,000 includes income tax and is not all taken from the pension.",
            "The exclusion for dependants' scheme pensions is now described the same way everywhere: it is not "
            "limited to defined benefit schemes.",
            "Paying the inheritance tax straight from the pension is shown as an option that the example uses, not "
            "a rule.",
            "The source of the £1 trillion estimate is given, and dated notes were added to the transcript on the "
            "same points.",
        ]),
        ("whole-of-life-assurance", [
            "'The trust gets back more than is paid in unless the life assured lives to nearly 102' is now tied to "
            "the particular age-75 quotation, with the warning that total premiums can exceed the payout.",
            "The page now names the type of policy it describes, a conventional policy with guaranteed, "
            "non-reviewable premiums, and says that 'the premiums are not lost' does not mean they are refunded.",
            "Premiums paid into a trust are now explained as gifts that are exempt only where an exemption "
            "applies, and the example's assumption that they qualify is stated.",
            "The 60% comparison now carries its assumptions, and the history of the 1980s is labelled as Steve's "
            "experience.",
            "Dated notes were added to the transcript on the same points.",
        ]),
        ("", [
            "Every answer now has a Sources line linking to the law on legislation.gov.uk and to HMRC's guidance "
            "on GOV.UK, with each source labelled.",
            "This page was added.",
        ]),
    ]),
]

if WOL_GUIDE_IN_BUILD:
    CORRECTIONS_LOG.insert(0, (f"{date.fromisoformat(WOL_GUIDE_RELEASE).day} "
                               f"{date.fromisoformat(WOL_GUIDE_RELEASE):%B %Y}",
                               "A new guide was published, and the whole of life video page gained links to it. "
                               "No answers on the existing pages were changed.", [
        (WOL_GUIDE_SLUG, [
            "Published: Whole of life assurance: every question answered. A guide of 32 questions drawn from Steve's "
            "LinkedIn articles and the video, each answer with its sources: premiums, insurable interest, trusts and "
            "inheritance tax, the tax on the payout, a dated example quotation and the history.",
        ]),
        ("whole-of-life-assurance", [
            "Guide links were added near the top, below the questions and under the related articles. The existing "
            "answers, key facts and transcript were unchanged.",
        ]),
    ]))

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def esc(s):
    # Escape &, <, > and double quotes only; apostrophes stay readable.
    return html.escape(s, quote=False).replace('"', "&quot;")


def mmss(seconds):
    return f"{seconds // 60}:{seconds % 60:02d}"


def yt_watch(vid, t=None):
    u = f"https://www.youtube.com/watch?v={vid}"
    if t:
        u += f"&t={t}s"
    return u


def nice_date(d):
    return d.strftime("%-d %B %Y")


def load_transcript(name):
    rows = []
    with open(os.path.join(HERE, "data", name), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            ts, text = line.split("\t", 1)
            m, s = ts.split(":")
            rows.append((int(m) * 60 + int(s), re.sub(r"\s+", " ", text).strip()))
    return rows


def paragraphs_from(cues, max_words=75):
    """Join cue fragments into readable paragraphs, breaking at sentence ends."""
    text = " ".join(t for _, t in cues)
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.?!])\s+(?=[A-Z£\"'(])", text)
    paras, current, count = [], [], 0
    for s in sentences:
        w = len(s.split())
        if current and count + w > max_words:
            paras.append(" ".join(current))
            current, count = [], 0
        current.append(s)
        count += w
    if current:
        paras.append(" ".join(current))
    return paras


def transcript_sections(video):
    cues = load_transcript(video["transcript_file"])
    chapters = video["chapters"]
    sections = []
    for i, (start, name) in enumerate(chapters):
        end = chapters[i + 1][0] if i + 1 < len(chapters) else 10 ** 9
        part = [c for c in cues if start <= c[0] < end]
        sections.append((start, name, paragraphs_from(part)))
    return sections


def plain_transcript(video):
    cues = load_transcript(video["transcript_file"])
    return re.sub(r"\s+", " ", " ".join(t for _, t in cues)).strip()


def unique(seq):
    out = []
    for x in seq:
        if x not in out:
            out.append(x)
    return out


def page_source_keys(v):
    keys = list(v["short_sources"])
    for _, ks in v.get("key_facts", []):
        keys += ks
    for _, _, ks in v.get("faq", []) + v.get("qa", []):
        keys += ks
    for n in v.get("notes", []):
        keys += n["sources"]
    return unique(keys)


def source_link(key):
    label, name, url = SOURCES[key]
    if url and url.startswith(SITE + "/"):
        return f'<a href="{esc(url[len(SITE):])}">{esc(name)}</a>'
    if url:
        return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(name)}</a>'
    return esc(name)


def sources_html(keys, tag="p"):
    """One compact line: Sources, grouped by label, in a fixed order."""
    keys = unique(keys)
    if not keys:
        return ""
    groups = {}
    for k in keys:
        groups.setdefault(SOURCES[k][0], []).append(k)
    parts = []
    for label in LABEL_ORDER:
        if label in groups:
            parts.append(f'<span class="lbl">{esc(label)}:</span> ' + "; ".join(source_link(k) for k in groups[label]))
    return f'<{tag} class="src"><span class="lead">Sources</span> ' + " &middot; ".join(parts) + f"</{tag}>"


def source_ld(key):
    label, name, url = SOURCES[key]
    if label == "Law":
        d = {"@type": "Legislation", "name": name}
    elif label == "Case law":
        d = {"@type": "CreativeWork", "genre": "Court judgment", "name": name}
    elif label == "HMRC":
        d = {"@type": "WebPage", "name": name,
             "publisher": {"@type": "GovernmentOrganization", "name": "HM Revenue and Customs"}}
    elif label.startswith("Steve's"):
        d = {"@type": "CreativeWork", "name": name, "author": {"@id": f"{SITE}/#steve-hunt"}}
    else:
        d = {"@type": "CreativeWork", "name": name}
    if url:
        d["url"] = url
    else:
        d["description"] = f"{label}, held on file by the author and not published."
    return d


NOTE_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def note_plain(text):
    """Note text without link markup, for structured data."""
    return NOTE_LINK.sub(r"\1", text)


def note_rich(text):
    """Note text with [words](href) turned into links, everything else escaped."""
    out, pos = [], 0
    for m in NOTE_LINK.finditer(text):
        out.append(esc(text[pos:m.start()]))
        out.append(f'<a href="{esc(m.group(2))}">{esc(m.group(1))}</a>')
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


def note_html(n):
    # Notes added after 1 October 2026 carry their own date; the older notes keep NOTE_DATE.
    when = nice_date(n["date"]) if "date" in n else NOTE_DATE
    anchor = f' id="{esc(n["id"])}"' if n.get("id") else ""
    return (f'<div class="correction" role="note"{anchor}><p><strong>{esc(n["kind"])}, {when}:</strong> '
            f'{note_rich(n["text"])}</p>{sources_html(n["sources"])}</div>')


# ---------------------------------------------------------------------------
# CSS (shared, inlined into every page)
# ---------------------------------------------------------------------------

CSS = """
:root{--navy:#0C192B;--navy2:#182C46;--gold:#C8A564;--ivory:#F3EBDA;--paper:#FFFDF8;--ink:#1B2433;--muted:#5A6577;--rule:#E3DCCB;--link:#0F4C81;--note:#FFF6E3}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--link)}
a:hover{text-decoration-thickness:2px}
h1,h2,h3{font-family:Caladea,Cambria,Georgia,"Times New Roman",serif;line-height:1.2;color:var(--navy);margin:0 0 .5em}
h1{font-size:2rem}
h2{font-size:1.5rem;margin-top:2.2em;padding-top:.6em;border-top:1px solid var(--rule)}
h3{font-size:1.15rem;margin-top:1.6em}
p,li{max-width:70ch}
.wrap{max-width:860px;margin:0 auto;padding:0 16px}
header.site{background:var(--navy);color:var(--ivory);padding:14px 0}
header.site .wrap{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:8px 20px}
header.site a{color:var(--ivory);text-decoration:none}
header.site .brand{font-family:Caladea,Georgia,serif;font-size:1.25rem;letter-spacing:.01em}
header.site .brand span{color:var(--gold)}
header.site nav{display:flex;flex-wrap:wrap;gap:4px 18px}
header.site nav a{font-size:.95rem;opacity:.92}
header.site nav a:hover{text-decoration:underline}
main{padding:28px 0 40px}
.kicker{color:var(--gold);font-weight:600;letter-spacing:.08em;text-transform:uppercase;font-size:.8rem;margin:0 0 .6em}
.byline{color:var(--muted);font-size:.95rem;margin:0 0 1.4em}
.answer{background:var(--ivory);border-left:4px solid var(--gold);padding:16px 20px;margin:1.4em 0}
.answer h2{margin:0 0 .5em;border:0;padding:0;font-size:1.2rem}
.answer p{margin:.5em 0}
.video{position:relative;padding-top:56.25%;background:var(--navy);margin:1.4em 0 .6em;border-radius:4px;overflow:hidden}
.video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.watch{font-size:.95rem;color:var(--muted);margin:0 0 1.5em}
ol.chapters{padding-left:0;list-style:none;margin:0}
ol.chapters li{margin:.35em 0}
ol.chapters .t{display:inline-block;min-width:3.6em;font-variant-numeric:tabular-nums;color:var(--muted)}
ul.facts li{margin:.7em 0}
.faq h3{margin-top:1.4em}
.src{display:block;color:var(--muted);font-size:.86rem;line-height:1.5;margin:.35em 0 1em;max-width:70ch;overflow-wrap:anywhere}
.src .lead{font-weight:700;color:var(--navy);margin-right:.35em;text-transform:uppercase;font-size:.75rem;letter-spacing:.06em}
.src .lbl{font-weight:600;color:var(--ink)}
ul.facts .src{margin:.2em 0 0}
.correction{background:var(--note);border-left:3px solid var(--gold);padding:10px 14px;margin:.6em 0 1.1em;max-width:70ch}
.correction p{margin:0 0 .3em;font-size:.95rem}
.correction .src{margin:.2em 0 0}
.srclist h3{font-size:1.05rem;margin:1.2em 0 .3em}
.srclist p.meaning{margin:0 0 .4em;color:var(--muted);font-size:.93rem}
.srclist ul{margin:.2em 0 .8em;padding-left:1.2em}
.srclist li{margin:.25em 0;overflow-wrap:anywhere}
.transcript h3{margin-top:1.8em}
.transcript h3 .t{font-family:inherit;font-weight:400;color:var(--muted);font-size:.9em;margin-right:.5em;font-variant-numeric:tabular-nums}
.note{color:var(--muted);font-size:.95rem}
.author{display:flex;gap:18px;align-items:flex-start;background:var(--ivory);padding:18px 20px;border-radius:4px;margin-top:2.5em}
.author h2{margin:0 0 .3em;border:0;padding:0;font-size:1.2rem}
.author p{margin:.4em 0;font-size:.97rem}
.disclaimer{border-top:1px solid var(--rule);margin-top:2em;padding-top:1em;color:var(--muted);font-size:.93rem}
.cards{display:grid;grid-template-columns:1fr;gap:22px;margin:1.5em 0}
@media(min-width:640px){.cards{grid-template-columns:1fr 1fr}}
.card{border:1px solid var(--rule);border-radius:6px;overflow:hidden;background:#fff}
.card img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
.card .body{padding:14px 16px 16px}
.card h2{border:0;padding:0;margin:0 0 .4em;font-size:1.15rem}
.card p{margin:.4em 0;font-size:.96rem}
footer.site{background:var(--navy);color:var(--ivory);padding:22px 0;font-size:.9rem}
footer.site a{color:var(--ivory)}
footer.site p{margin:.3em 0;max-width:none}
.related{margin-top:1.5em;padding:12px 16px;border:1px solid var(--rule);border-radius:4px}
.related p{margin:.2em 0}
.log li{margin:.5em 0}
"""

HEAD_BASE = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caladea:wght@400;700&display=swap" rel="stylesheet">
"""
ROBOTS_INDEX = '<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1">\n'
HEAD_COMMON = HEAD_BASE + ROBOTS_INDEX


def header_html():
    return f"""<header class="site"><div class="wrap">
<a class="brand" href="/">{esc(SITE_NAME)} <span>by Steve Hunt ACII TEP</span></a>
<nav><a href="/">Home</a><a href="/pensions-and-inheritance-tax-from-april-2027/">Pensions and IHT 2027</a><a href="/nominees-annuity/">Nominees' annuity</a><a href="/whole-of-life-assurance/">Whole of life</a><a href="{ABOUT_PATH}">About Steve</a></nav>
</div></header>"""


def footer_html():
    return f"""<footer class="site"><div class="wrap">
<p>{esc(SITE_NAME)}. Plain English explanations of UK inheritance tax by Steve Hunt ACII TEP.</p>
<p>Education only. Not advice, not a personal recommendation, and not an invitation to do business. Tax rules change; check the date on each page.</p>
<p><a href="{ABOUT_PATH}">About Steve Hunt</a> &middot; <a href="{CORRECTIONS_PATH}">Sources, method and corrections</a> &middot; <a href="{LINKEDIN}" rel="me">Steve Hunt on LinkedIn</a> &middot; <a href="{YOUTUBE_CHANNEL}" rel="me">YouTube channel</a> &middot; <a href="{X_PROFILE}" rel="me">X</a> &middot; &copy; 2026 Stephen Hunt</p>
</div></footer>"""


def author_box():
    return f"""<section class="author" id="about-the-author">
<div>
<h2>About Steve Hunt ACII TEP</h2>
<p>Steve Hunt is a Chartered Insurance Risk Manager, an Associate of the Chartered Insurance Institute (ACII), and a Trust and Estate Practitioner (TEP), a full member of STEP. He has worked in UK financial services since 1980, in pensions, protection and estate planning. He writes about inheritance tax, the April 2027 pension changes, annuities, whole of life assurance and trusts.</p>
<p><a href="{ABOUT_PATH}">More about Steve</a> &middot; <a href="{LINKEDIN}" rel="me">LinkedIn profile and articles</a> &middot; <a href="{YOUTUBE_CHANNEL}" rel="me">YouTube channel</a> &middot; <a href="{X_PROFILE}" rel="me">X</a> &middot; <a href="{CORRECTIONS_PATH}">How these answers are sourced</a></p>
</div>
</section>"""


DISCLAIMER = """<p class="disclaimer">This page and the video are education only. They are not advice, not a personal recommendation, and not an invitation to do business. They describe the law and HMRC's published position as at {asat}, which can change. Nothing here takes account of your circumstances. The narration in the video uses a digital clone of Steve Hunt's voice. The words are his own.</p>"""


# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------

def person_ld():
    return {
        "@type": "Person",
        "@id": f"{SITE}/#steve-hunt",
        "name": "Steve Hunt",
        "alternateName": ["Steve Hunt ACII TEP", "Stephen Hunt"],
        "honorificSuffix": "ACII TEP",
        "jobTitle": "Chartered Insurance Risk Manager and Trust and Estate Practitioner",
        "description": "UK financial services professional since 1980. Chartered Insurance Risk Manager, Associate of the Chartered Insurance Institute (ACII) and Trust and Estate Practitioner (TEP). Writes and presents plain English explanations of inheritance tax, the April 2027 pension changes, annuities, whole of life assurance and trusts.",
        "url": ABOUT_URL,
        "mainEntityOfPage": ABOUT_URL,
        "sameAs": [LINKEDIN, YOUTUBE_CHANNEL, X_PROFILE],
        "knowsAbout": ["Inheritance tax", "Pensions and inheritance tax from April 2027", "Nominees' annuities",
                       "Joint life annuities", "Whole of life assurance", "Trusts and estate planning"],
        "memberOf": [
            {"@type": "Organization", "name": "The Chartered Insurance Institute", "url": "https://www.cii.co.uk/"},
            {"@type": "Organization", "name": "STEP, the Society of Trust and Estate Practitioners", "url": STEP_SITE},
        ],
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "name": "ACII, Associate of the Chartered Insurance Institute",
             "credentialCategory": "Professional membership",
             "recognizedBy": {"@type": "Organization", "name": "The Chartered Insurance Institute",
                              "url": "https://www.cii.co.uk/"}},
            {"@type": "EducationalOccupationalCredential", "name": "Chartered Insurance Risk Manager",
             "credentialCategory": "Chartered title",
             "recognizedBy": {"@type": "Organization", "name": "The Chartered Insurance Institute",
                              "url": "https://www.cii.co.uk/"}},
            {"@type": "EducationalOccupationalCredential", "name": "TEP, Trust and Estate Practitioner (STEP)",
             "credentialCategory": "Professional membership",
             "recognizedBy": {"@type": "Organization", "name": "STEP, the Society of Trust and Estate Practitioners",
                              "url": STEP_SITE}},
        ],
    }


def website_ld():
    return {
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "url": SITE + "/",
        "name": SITE_NAME,
        "description": "Plain English explanations of UK inheritance tax, the April 2027 pension changes, annuities, whole of life assurance and trusts, with videos, key facts and full transcripts. Every answer links to the law and HMRC guidance it relies on. By Steve Hunt ACII TEP. Education only.",
        "inLanguage": "en-GB",
        "author": {"@id": f"{SITE}/#steve-hunt"},
        "publishingPrinciples": CORRECTIONS_URL,
    }


def video_ld(v):
    url = f"{SITE}/{v['slug']}/"
    clips = []
    for i, (start, name) in enumerate(v["chapters"]):
        end = v["chapters"][i + 1][0] if i + 1 < len(v["chapters"]) else v["seconds"]
        clips.append({
            "@type": "Clip",
            "name": name,
            "startOffset": start,
            "endOffset": end,
            "url": yt_watch(v["id"], start),
        })
    video = {
        "@type": "VideoObject",
        "@id": f"{url}#video",
        "name": v["title"],
        "description": v["meta_description"],
        "thumbnailUrl": [f"{SITE}/images/{v['slug']}.jpg", f"https://i.ytimg.com/vi/{v['id']}/maxresdefault.jpg"],
        "uploadDate": v["published_iso"],
        "datePublished": v["published_iso"],
        "duration": v["duration_iso"],
        "embedUrl": f"https://www.youtube-nocookie.com/embed/{v['id']}",
        "url": yt_watch(v["id"]),
        "inLanguage": "en-GB",
        "isFamilyFriendly": True,
        "author": {"@id": f"{SITE}/#steve-hunt"},
        "creator": {"@id": f"{SITE}/#steve-hunt"},
        "publisher": {"@id": f"{SITE}/#steve-hunt"},
        "keywords": ", ".join(v["keywords"]),
        "learningResourceType": "Concept overview",
        "educationalUse": "self-study",
        "hasPart": clips,
        "transcript": plain_transcript(v),
        "correction": [
            {"@type": "CorrectionComment", "text": f"{n['kind']}: {note_plain(n['text'])}",
             "datePublished": n.get("date", REVIEWED).isoformat()}
            for n in v["notes"]
        ],
    }
    faq = {
        "@type": "FAQPage",
        "@id": f"{url}#faq",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": dict({"@type": "Answer", "text": a},
                                    **({"citation": [source_ld(k) for k in unique(ks)]} if ks else {}))}
            for q, a, ks in v["faq"]
        ],
    }
    citations = [{"@type": "CreativeWork", "name": ARTICLES[k][0], "url": ARTICLES[k][1],
                  "author": {"@id": f"{SITE}/#steve-hunt"}} for k, _ in v["articles"]]
    citations += [source_ld(k) for k in page_source_keys(v)]
    page = {
        "@type": ["WebPage", "LearningResource"],
        "@id": url,
        "url": url,
        "name": v["title"],
        "description": v["meta_description"],
        "inLanguage": "en-GB",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "author": {"@id": f"{SITE}/#steve-hunt"},
        "datePublished": v["published"],
        "dateModified": v["modified"],
        "lastReviewed": REVIEWED.isoformat(),
        "reviewedBy": {"@id": f"{SITE}/#steve-hunt"},
        "publishingPrinciples": CORRECTIONS_URL,
        "video": {"@id": f"{url}#video"},
        "mainEntity": {"@id": f"{url}#video"},
        "learningResourceType": "Concept overview",
        "about": [{"@type": "Thing", "name": k} for k in v["keywords"][:4]],
        "citation": citations,
    }
    return {"@context": "https://schema.org", "@graph": [website_ld(), person_ld(), page, video, faq]}


def home_ld():
    items = [{
        "@type": "ListItem", "position": v["number"], "url": f"{SITE}/{v['slug']}/", "name": v["title"],
    } for v in VIDEOS]
    page = {
        "@type": "CollectionPage",
        "@id": SITE + "/",
        "url": SITE + "/",
        "name": f"{SITE_NAME} by Steve Hunt ACII TEP",
        "description": website_ld()["description"],
        "inLanguage": "en-GB",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "author": {"@id": f"{SITE}/#steve-hunt"},
        "dateModified": TODAY.isoformat(),
        "publishingPrinciples": CORRECTIONS_URL,
        "mainEntity": {"@type": "ItemList", "itemListElement": items},
    }
    return {"@context": "https://schema.org", "@graph": [website_ld(), person_ld(), page]}


def ld_script(obj):
    txt = json.dumps(obj, ensure_ascii=False, indent=1)
    txt = txt.replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{txt}\n</script>'


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def page_sources_section(v):
    keys = page_source_keys(v)
    groups = {}
    for k in keys:
        groups.setdefault(SOURCES[k][0], []).append(k)
    out = ['<section class="srclist" id="sources">', "<h2>Sources and evidence</h2>",
           f'<p class="note">Every source behind this page, grouped by the kind of authority it carries. '
           f'<a href="{CORRECTIONS_PATH}">How the sources are labelled, and what has been corrected</a>.</p>']
    for label in LABEL_ORDER:
        if label not in groups:
            continue
        out.append(f"<h3>{esc(label)}</h3>")
        out.append(f'<p class="meaning">{esc(LABEL_MEANING[label][0].upper() + LABEL_MEANING[label][1:])}.</p>')
        out.append("<ul>" + "".join(f"<li>{source_link(k)}</li>" for k in groups[label]) + "</ul>")
    out.append("</section>")
    return "\n".join(out)


def transcript_html_for(v):
    sections = transcript_sections(v)
    placed = set()
    parts = []
    for start, name, paras in sections:
        link = yt_watch(v["id"], start) if start else yt_watch(v["id"])
        parts.append(
            f'<h3 id="t{start}"><a class="t" href="{link}" target="_blank" rel="noopener">{mmss(start)}</a>{esc(name)}</h3>'
        )
        for p in paras:
            parts.append(f"<p>{esc(p)}</p>")
            for i, n in enumerate(v["notes"]):
                if i not in placed and n["phrase"] in p:
                    parts.append(note_html(n))
                    placed.add(i)
    missing = [v["notes"][i]["phrase"] for i in range(len(v["notes"])) if i not in placed]
    assert not missing, f"transcript note phrases not found in {v['slug']}: {missing}"
    return "\n".join(parts)


def video_page(v):
    url = f"{SITE}/{v['slug']}/"
    thumb = f"{SITE}/images/{v['slug']}.jpg"
    pub_text = nice_date(date.fromisoformat(v["published"]))

    chapters_html = "\n".join(
        f'<li><a class="t" href="{yt_watch(v["id"], s) if s else yt_watch(v["id"])}" target="_blank" rel="noopener">{mmss(s)}</a> '
        f'<a href="#t{s}">{esc(n)}</a></li>'
        for s, n in v["chapters"]
    )
    facts_html = "\n".join(
        f"<li>{esc(f)}{sources_html(ks, tag='span')}</li>" for f, ks in v["key_facts"]
    )
    faq_html = "\n".join(
        f"<h3>{esc(q)}</h3>\n<p>{esc(a)}</p>\n{sources_html(ks)}" for q, a, ks in v["faq"]
    )
    articles_html = "\n".join(
        f'<li><a href="{ARTICLES[k][1]}" target="_blank" rel="noopener">{esc(ARTICLES[k][0])}</a> {esc(note)}</li>'
        for k, note in v["articles"]
    )
    related_html = "".join(
        f'<p><strong>{esc(label)}:</strong> <a href="/{slug}/">{esc(title)}</a></p>'
        for label, slug, title in v["related"]
    )
    guide_note = ""
    guide_top = ""
    if v.get("guide"):
        gslug, gtitle = v["guide"]
        guide_note = (f'\n<p class="note"><strong>More questions are answered in the full guide:</strong> '
                      f'<a href="/{gslug}/">{esc(gtitle)}</a>.</p>')
        guide_top = (f'\n<div class="related"><p><strong>Read the full guide:</strong> '
                     f'<a href="/{gslug}/">{esc(gtitle)}</a>, each answer with its sources.</p></div>\n')
        related_html = f'<p><strong>Full guide:</strong> <a href="/{gslug}/">{esc(gtitle)}</a></p>' + related_html
    transcript_html = transcript_html_for(v)
    ld = ld_script(video_ld(v))

    return f"""<!doctype html>
<html lang="en-GB">
<head>
{HEAD_COMMON}<title>{esc(v['seo_title'])}</title>
<meta name="description" content="{esc(v['seo_description'])}">
<meta name="author" content="{esc(AUTHOR)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="video.other">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{esc(v['title'])}">
<meta property="og:description" content="{esc(v['seo_description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{thumb}">
<meta property="og:video:url" content="https://www.youtube-nocookie.com/embed/{v['id']}">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(v['title'])}">
<meta name="twitter:description" content="{esc(v['seo_description'])}">
<meta name="twitter:image" content="{thumb}">
<style>{CSS}</style>
{ld}
</head>
<body>
{header_html()}
<main class="wrap">
<article>
<p class="kicker">Video {v['number']} &middot; Inheritance tax explained</p>
<h1>{esc(v['title'])}</h1>
<p class="byline">By <a href="#about-the-author">Steve Hunt ACII TEP</a> &middot; Published {pub_text} &middot; <a href="{CORRECTIONS_PATH}">Last reviewed {nice_date(REVIEWED)}</a> &middot; Video {v['duration_text']} &middot; Full transcript below</p>

<section class="answer" id="short-answer">
<h2>The short answer</h2>
{''.join(f'<p>{esc(p)}</p>' for p in v['short_answer'])}
{sources_html(v['short_sources'])}
</section>
{guide_top}
<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{v['id']}?rel=0" title="{esc(v['title'])}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>
<p class="watch"><a href="{yt_watch(v['id'])}" target="_blank" rel="noopener">Watch on YouTube</a> &middot; <a href="{PLAYLIST}" target="_blank" rel="noopener">All videos in the series</a></p>

<h2 id="chapters">In this video</h2>
<ol class="chapters">
{chapters_html}
</ol>

<h2 id="key-facts">Key facts (as at {v.get('as_at', AS_AT)})</h2>
<ul class="facts">
{facts_html}
</ul>
<p class="note">{esc(v['assumptions'])}</p>
<p class="note">Legislation referred to: {esc(v['legislation'])}</p>

<section class="faq" id="questions">
<h2>Questions this video answers</h2>
{faq_html}{guide_note}
</section>

{page_sources_section(v)}

<h2 id="articles">Steve's LinkedIn articles behind this video</h2>
<ul>
{articles_html}
</ul>

<div class="related">{related_html}</div>

<section class="transcript" id="transcript">
<h2>Full transcript</h2>
<p class="note">This is what is said in the video, with the figures written as numbers. Timestamps open the video at that point. The words are not changed after publication: where something said needs correcting or qualifying, a dated note sits beside it. The narration uses a digital clone of Steve Hunt's voice. The words are his own.</p>
{transcript_html}
</section>

{author_box()}
{DISCLAIMER.format(asat=v.get('as_at', AS_AT))}
</article>
</main>
{footer_html()}
</body>
</html>
"""


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:70].rstrip("-")


# Guide answers can hold more than one paragraph, simple lists and a table. Plain one-paragraph answers render
# exactly as before.
BOLD = re.compile(r"\*\*(.+?)\*\*")
GUIDE_TABLE_CSS = """
.tablewrap{overflow-x:auto;margin:1em 0 .4em}
table.figures{border-collapse:collapse;width:100%;font-size:.95rem}
table.figures th,table.figures td{border-bottom:1px solid var(--rule);padding:8px 10px;text-align:left;vertical-align:top}
table.figures thead th{border-bottom:2px solid var(--gold)}
"""


def rich_inline(s):
    out, pos = [], 0
    for m in BOLD.finditer(s):
        out.append(esc(s[pos:m.start()]))
        out.append(f"<strong>{esc(m.group(1))}</strong>")
        pos = m.end()
    out.append(esc(s[pos:]))
    return "".join(out)


def rich_blocks(text):
    """Split rich text into ('p', text), ('ul', [(item, [subitems])]) and ('table', [rows]) blocks."""
    blocks = []
    for raw in text.split("\n\n"):
        lines = raw.split("\n")
        if all(ln.startswith("|") for ln in lines):
            rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
            assert set(rows[1][0]) <= set("-:"), raw
            blocks.append(("table", [rows[0]] + rows[2:]))
        elif all(ln.startswith("- ") or ln.startswith("  - ") for ln in lines):
            items = []
            for ln in lines:
                if ln.startswith("  - "):
                    items[-1][1].append(ln[4:])
                else:
                    items.append((ln[2:], []))
            blocks.append(("ul", items))
        else:
            assert "\n" not in raw, raw
            blocks.append(("p", raw))
    return blocks


def rich_html(text):
    out = []
    for kind, val in rich_blocks(text):
        if kind == "p":
            out.append(f"<p>{rich_inline(val)}</p>")
        elif kind == "ul":
            lis = []
            for item, subs in val:
                sub = ("<ul>" + "".join(f"<li>{rich_inline(s)}</li>" for s in subs) + "</ul>") if subs else ""
                lis.append(f"<li>{rich_inline(item)}{sub}</li>")
            out.append("<ul>" + "".join(lis) + "</ul>")
        else:
            head, rows = val[0], val[1:]
            out.append('<div class="tablewrap"><table class="figures"><thead><tr>'
                       + "".join(f'<th scope="col">{rich_inline(c)}</th>' for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{rich_inline(c)}</td>" for c in r) + "</tr>" for r in rows)
                       + "</tbody></table></div>")
    return "\n".join(out)


def rich_plain(text):
    """The same words as plain text, for structured data. A table row reads 'Heading: value; ...'."""
    parts = []
    for kind, val in rich_blocks(text):
        if kind == "p":
            parts.append(BOLD.sub(r"\1", val))
        elif kind == "ul":
            for item, subs in val:
                parts.append(BOLD.sub(r"\1", item))
                parts += [BOLD.sub(r"\1", s) for s in subs]
        else:
            head, rows = val[0], val[1:]
            parts += ["; ".join(f"{h}: {c}" for h, c in zip(head, r)) + "." for r in rows]
    return " ".join(parts)


def guide_has_table(g):
    return any(kind == "table" for _, a, _ in g["qa"] for kind, _ in rich_blocks(a))


def guide_ld(g):
    url = f"{SITE}/{g['slug']}/"
    parent = next(v for v in VIDEOS if v["slug"] == g["parent"])
    faq = {
        "@type": "FAQPage",
        "@id": f"{url}#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "url": f"{url}#{slugify(q)}",
             "acceptedAnswer": dict({"@type": "Answer", "text": rich_plain(a)},
                                    **({"citation": [source_ld(k) for k in unique(ks)]} if ks else {}))}
            for q, a, ks in g["qa"]
        ],
    }
    citations = [{"@type": "CreativeWork", "name": ARTICLES[k][0], "url": ARTICLES[k][1],
                  "author": {"@id": f"{SITE}/#steve-hunt"}} for k, _ in g["articles"]]
    citations += [source_ld(k) for k in page_source_keys(g)]
    page = {
        "@type": ["WebPage", "LearningResource", "Article"],
        "@id": url,
        "url": url,
        "name": g["title"],
        "headline": g["title"],
        "description": g["meta_description"],
        "inLanguage": "en-GB",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "author": {"@id": f"{SITE}/#steve-hunt"},
        "publisher": {"@id": f"{SITE}/#steve-hunt"},
        "datePublished": g["published"],
        "dateModified": g["modified"],
        "lastReviewed": g["reviewed"],
        "reviewedBy": {"@id": f"{SITE}/#steve-hunt"},
        "publishingPrinciples": CORRECTIONS_URL,
        "mainEntity": {"@id": f"{url}#faq"},
        "learningResourceType": "Reference guide",
        "about": [{"@type": "Thing", "name": k} for k in g["keywords"][:4]],
        "keywords": ", ".join(g["keywords"]),
        "video": {"@id": f"{SITE}/{parent['slug']}/#video"},
        "citation": citations,
    }
    return {"@context": "https://schema.org", "@graph": [website_ld(), person_ld(), page, faq]}


def guide_page(g):
    url = f"{SITE}/{g['slug']}/"
    parent = next(v for v in VIDEOS if v["slug"] == g["parent"])
    thumb = f"{SITE}/images/{parent['slug']}.jpg"
    pub_text = nice_date(date.fromisoformat(g["published"]))
    contents_html = "\n".join(
        f'<li><a href="#{slugify(q)}">{esc(q)}</a></li>' for q, _, _ in g["qa"]
    )
    qa_html = "\n".join(
        f'<h3 id="{slugify(q)}">{esc(q)}</h3>\n{rich_html(a)}\n{sources_html(ks)}' for q, a, ks in g["qa"]
    )
    articles_html = "\n".join(
        f'<li><a href="{ARTICLES[k][1]}" target="_blank" rel="noopener">{esc(ARTICLES[k][0])}</a> {esc(note)}</li>'
        for k, note in g["articles"]
    )
    ld = ld_script(guide_ld(g))
    css = CSS + (GUIDE_TABLE_CSS if guide_has_table(g) else "")
    return f"""<!doctype html>
<html lang="en-GB">
<head>
{HEAD_COMMON}<title>{esc(g['seo_title'])}</title>
<meta name="description" content="{esc(g['seo_description'])}">
<meta name="author" content="{esc(AUTHOR)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{esc(g['title'])}">
<meta property="og:description" content="{esc(g['seo_description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{thumb}">
<meta property="og:locale" content="en_GB">
<meta property="article:published_time" content="{g['published']}">
<meta property="article:modified_time" content="{g['modified']}">
<meta property="article:author" content="{LINKEDIN}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(g['title'])}">
<meta name="twitter:description" content="{esc(g['seo_description'])}">
<meta name="twitter:image" content="{thumb}">
<style>{css}</style>
{ld}
</head>
<body>
{header_html()}
<main class="wrap">
<article>
<p class="kicker">Guide &middot; Inheritance tax explained</p>
<h1>{esc(g['title'])}</h1>
<p class="byline">By <a href="#about-the-author">Steve Hunt ACII TEP</a> &middot; Published {pub_text} &middot; <a href="{CORRECTIONS_PATH}">Last reviewed {nice_date(date.fromisoformat(g['reviewed']))}</a> &middot; {len(g['qa'])} questions</p>
{rich_html(g['intro'])}

<section class="answer" id="short-answer">
<h2>The short answer</h2>
{''.join(f'<p>{esc(p)}</p>' for p in g['short_answer'])}
{sources_html(g['short_sources'])}
</section>

<div class="related"><p><strong>The video:</strong> <a href="/{parent['slug']}/">{esc(parent['title'])}</a>, with key facts and the full transcript.</p></div>

<h2 id="contents">The questions</h2>
<ol class="chapters">
{contents_html}
</ol>

<section class="faq" id="questions">
<h2>The answers</h2>
{qa_html}
</section>

{page_sources_section(g)}

<h2 id="articles">Steve's LinkedIn articles behind this guide</h2>
<ul>
{articles_html}
</ul>

{author_box()}
<p class="disclaimer">This guide is education only. It is not advice, not a personal recommendation, and not an invitation to do business. It describes the law and HMRC's published position as at {esc(nice_date(date.fromisoformat(g['reviewed'])))}, which can change, and it says where an answer is Steve's own reading rather than settled law. Nothing here takes account of your circumstances.</p>
</article>
</main>
{footer_html()}
</body>
</html>
"""


def home_page():
    cards = []
    for v in VIDEOS:
        cards.append(f"""<article class="card">
<a href="/{v['slug']}/"><img src="/images/{v['slug']}.jpg" alt="{esc(v['title'])}" width="1280" height="720" loading="lazy"></a>
<div class="body">
<h2><a href="/{v['slug']}/">{esc(v['title'])}</a></h2>
<p>{esc(v['short_answer'][0])}</p>
<p><a href="/{v['slug']}/">Video, key facts, sources and full transcript</a> &middot; {v['duration_text']}</p>
{(f'<p><a href="/{v["guide"][0]}/">Full guide: {esc(v["guide"][1])}</a></p>' if v.get("guide") else "")}
</div>
</article>""")
    cards_html = "\n".join(cards)
    ld = ld_script(home_ld())
    desc = HOME_DESCRIPTION
    return f"""<!doctype html>
<html lang="en-GB">
<head>
{HEAD_COMMON}<title>{esc(SITE_NAME)} by Steve Hunt ACII TEP</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="{esc(AUTHOR)}">
<link rel="canonical" href="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{esc(SITE_NAME)} by Steve Hunt ACII TEP">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/images/{VIDEOS[0]['slug']}.jpg">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<style>{CSS}</style>
{ld}
</head>
<body>
{header_html()}
<main class="wrap">
<p class="kicker">Steve Hunt ACII TEP</p>
<h1>Inheritance tax, explained in plain English</h1>
<p>Short videos that answer the questions families actually ask about UK inheritance tax: what the rules say, what things cost, and how the pieces fit together. The big one right now is the April 2027 change that brings most unused pension funds and pension death benefits into inheritance tax.</p>
<p>Every video on this site comes with its key facts, the questions it answers and a full transcript, so you can read it as well as watch it. Every answer links to the law and the HMRC guidance it relies on, so you can check it for yourself. <a href="{CORRECTIONS_PATH}">How the sources are labelled, and what has been corrected</a>.</p>

<h2 id="videos" style="border:0;margin-top:1.6em">The videos</h2>
<div class="cards">
{cards_html}
</div>
<p><a href="{PLAYLIST}" target="_blank" rel="noopener">The series playlist on YouTube</a> &middot; <a href="{LINKEDIN}" target="_blank" rel="noopener">Steve's LinkedIn articles</a></p>

{author_box()}
<p class="disclaimer">Everything on this site is education only. It is not advice, not a personal recommendation, and not an invitation to do business. Tax rules change, and nothing here takes account of your circumstances.</p>
</main>
{footer_html()}
</body>
</html>
"""


def corrections_page():
    url = CORRECTIONS_URL
    title = "Sources, method and corrections"
    seo_title = f"{title} | {SITE_NAME}"
    desc = ("How each answer on this site is backed up: the law first, then HMRC's published view, dated "
            "evidence and clearly labelled analysis. Plus a corrections log.")
    labels_html = "\n".join(
        f"<li><strong>{esc(label)}:</strong> {esc(LABEL_MEANING[label])}.</li>" for label in LABEL_ORDER
    )
    titles = {v["slug"]: v["short_title"] for v in VIDEOS}
    log_html = []
    titles.update({g["slug"]: g["short_title"] for g in GUIDES})
    if INCLUDE_EVIDENCE:
        titles[EVIDENCE_SLUG] = "Nominees' annuity quotations"
    for when, intro, groups in CORRECTIONS_LOG:
        log_html.append(f"<h3>{esc(when)}</h3>")
        log_html.append(f"<p>{esc(intro)}</p>")
        for slug, items in groups:
            heading = (f'<a href="/{slug}/">{esc(titles[slug])}</a>' if slug else "All pages")
            log_html.append(f"<p><strong>{heading}</strong></p>")
            log_html.append('<ul class="log">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>")
    log_html = "\n".join(log_html)
    ld = {
        "@context": "https://schema.org",
        "@graph": [website_ld(), person_ld(), {
            "@type": "WebPage",
            "@id": url,
            "url": url,
            "name": title,
            "description": desc,
            "inLanguage": "en-GB",
            "isPartOf": {"@id": f"{SITE}/#website"},
            "author": {"@id": f"{SITE}/#steve-hunt"},
            "about": {"@id": f"{SITE}/#website"},
            "datePublished": "2026-10-01",  # first published 1 October 2026; never moves (R01)
            "dateModified": TODAY.isoformat(),
            "lastReviewed": REVIEWED.isoformat(),
        }],
    }
    return f"""<!doctype html>
<html lang="en-GB">
<head>
{HEAD_COMMON}<title>{esc(seo_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="{esc(AUTHOR)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_GB">
<style>{CSS}</style>
{ld_script(ld)}
</head>
<body>
{header_html()}
<main class="wrap">
<article>
<p class="kicker">About this site</p>
<h1>{esc(title)}</h1>
<p class="byline">By <a href="#about-the-author">Steve Hunt ACII TEP</a> &middot; Last updated {nice_date(TODAY)}</p>
<p>Every answer on this site is written by Steve Hunt ACII TEP, a Chartered Insurance Risk Manager and Trust and Estate Practitioner who has worked in UK financial services since 1980. This page explains where the answers come from, how they are backed up, and what has been corrected.</p>

<h2 id="how">How each answer is backed up</h2>
<p>Beside each answer is a Sources line, and each page ends with a full list of its sources. Every source carries one of these labels, so you can see what kind of authority stands behind each statement:</p>
<ul>
{labels_html}
</ul>
<p>Where the law is clear, it comes first, linked to the official text. Where HMRC's published view and Steve's reading differ, both are shown and labelled.</p>

<h2 id="transcripts">Videos and transcripts</h2>
<p>Each video page carries the full transcript of its video. The transcript records what is said in the video, and its words are not changed after publication. If something said in a video needs correcting or qualifying, a dated note is added beside the words it relates to.</p>

<h2 id="dates">Dates</h2>
<p>Each page shows when it was published and when it was last reviewed. The review date changes only when the page has actually been reviewed, not to make it look fresh. Tax rules change, so always check the date.</p>

<h2 id="corrections">Corrections and updates</h2>
{log_html}

<h2 id="errors">Spotted an error?</h2>
<p>Comment on the video on <a href="{YOUTUBE_CHANNEL}" rel="me">YouTube</a> or on the article on <a href="{LINKEDIN}" rel="me">LinkedIn</a>. Comments are read, and anything wrong will be put right and logged here.</p>

{author_box()}
<p class="disclaimer">Everything on this site is education only. It is not advice, not a personal recommendation, and not an invitation to do business. Tax rules change, and nothing here takes account of your circumstances.</p>
</article>
</main>
{footer_html()}
</body>
</html>
"""


def about_page():
    url = ABOUT_URL
    title = "About Steve Hunt ACII TEP"
    seo_title = f"{title} | {SITE_NAME}"
    desc = ("Steve Hunt ACII TEP is a Chartered Insurance Risk Manager and Trust and Estate Practitioner, in UK "
            "financial services since 1980. What he writes about here.")
    bio = ("Steve Hunt is a Chartered Insurance Risk Manager, an Associate of the Chartered Insurance Institute "
           "(ACII), and a Trust and Estate Practitioner (TEP), a full member of STEP. He has worked in UK financial "
           "services since 1980, in pensions, protection and estate planning. He writes about inheritance tax, the "
           "April 2027 pension changes, annuities, whole of life assurance and trusts.")
    pages = [f'<li><a href="/{g["slug"]}/">{esc(g["title"])}</a>: a guide, every question answered with its sources</li>'
             for g in GUIDES]
    pages += [f'<li><a href="/{v["slug"]}/">{esc(v["title"])}</a>: the video, its key facts and the full transcript</li>'
              for v in VIDEOS]
    articles = [f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t, u in ARTICLES.values()]
    page = {
        "@type": "ProfilePage",
        "@id": url,
        "url": url,
        "name": title,
        "description": desc,
        "inLanguage": "en-GB",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "mainEntity": {"@id": f"{SITE}/#steve-hunt"},
        "about": {"@id": f"{SITE}/#steve-hunt"},
        "dateCreated": ABOUT_PUBLISHED,
        "datePublished": ABOUT_PUBLISHED,
        "dateModified": TODAY.isoformat(),
        "publishingPrinciples": CORRECTIONS_URL,
    }
    ld = {"@context": "https://schema.org", "@graph": [website_ld(), person_ld(), page]}
    return f"""<!doctype html>
<html lang="en-GB">
<head>
{HEAD_COMMON}<title>{esc(seo_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="{esc(AUTHOR)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_GB">
<meta property="profile:first_name" content="Steve">
<meta property="profile:last_name" content="Hunt">
<style>{CSS}</style>
{ld_script(ld)}
</head>
<body>
{header_html()}
<main class="wrap">
<article>
<p class="kicker">About the author</p>
<h1>Steve Hunt ACII TEP</h1>
<p class="byline">Chartered Insurance Risk Manager and Trust and Estate Practitioner &middot; Last updated {nice_date(TODAY)}</p>
<p>{esc(bio)}</p>

<h2 id="qualifications">Qualifications</h2>
<ul>
<li><strong>ACII:</strong> Associate of the Chartered Insurance Institute, the professional body for the insurance and financial planning profession. <a href="{CII_TITLES}" target="_blank" rel="noopener">The Institute's designations and titles</a>.</li>
<li><strong>Chartered Insurance Risk Manager:</strong> a chartered title awarded by the Chartered Insurance Institute to qualified members. <a href="{CIRM_REGISTER}" target="_blank" rel="noopener">The title on the GOV.UK register of regulated professions</a>.</li>
<li><strong>TEP:</strong> Trust and Estate Practitioner. Only full members of STEP, the Society of Trust and Estate Practitioners, can use these letters. <a href="{STEP_SITE}" target="_blank" rel="noopener">STEP</a>.</li>
</ul>

<h2 id="experience">Experience</h2>
<p>Steve has worked in UK financial services since 1980, in pensions, protection and estate planning. Where an answer on this site draws on that experience rather than on the law or HMRC's published guidance, its source is labelled Steve's experience.</p>

<h2 id="writing">What he writes about here</h2>
<p>Plain English explanations of UK inheritance tax: the April 2027 change that brings unused pension funds into the estate, the nominees' annuity, whole of life assurance and trusts. Each subject has a page built around a video, with its key facts, the questions it answers and a full transcript. The biggest subjects also have a guide that answers every question, each answer with its sources.</p>
<ul>
{chr(10).join(pages)}
</ul>

<h2 id="articles">LinkedIn articles behind these pages</h2>
<p>The pages draw on Steve's LinkedIn articles, which set out his reasoning at greater length.</p>
<ul>
{chr(10).join(articles)}
</ul>
<p><a href="{LINKEDIN}" rel="me">All of Steve's articles on LinkedIn</a></p>

<h2 id="method">How the answers are backed up</h2>
<p>Every answer gives its sources, each labelled by the kind of authority it carries: the law, case law, HMRC's published view, dated provider evidence, published sources, or Steve's own analysis or experience. Where his reading goes beyond settled law, it is labelled as his analysis, with HMRC's published position beside it. Corrections are dated and logged. <a href="{CORRECTIONS_PATH}">Sources, method and corrections</a>.</p>

<h2 id="elsewhere">Elsewhere</h2>
<ul>
<li><a href="{LINKEDIN}" rel="me">Steve Hunt on LinkedIn</a></li>
<li><a href="{YOUTUBE_CHANNEL}" rel="me">Steve Hunt ACII TEP on YouTube</a></li>
<li><a href="{X_PROFILE}" rel="me">Steve Hunt ACII TEP on X</a></li>
</ul>

<p class="disclaimer">Everything on this site is education only. It is not advice, not a personal recommendation, and not an invitation to do business. Tax rules change, and nothing here takes account of your circumstances.</p>
</article>
</main>
{footer_html()}
</body>
</html>
"""


EVIDENCE_CSS = """
.tablewrap{overflow-x:auto;margin:1em 0 .4em}
table.ev{border-collapse:collapse;width:100%;font-size:.95rem}
table.ev th,table.ev td{border-bottom:1px solid var(--rule);padding:8px 10px;text-align:left;vertical-align:top}
table.ev thead th{border-bottom:2px solid var(--gold)}
table.ev tbody th{font-weight:600;width:36%}
table.ev caption{caption-side:top;text-align:left;color:var(--muted);font-size:.9rem;padding:0 0 .4em}
"""


def evidence_page():
    url = EVIDENCE_URL
    guide = next(g for g in ALL_GUIDES if g["slug"] == "nominees-annuity/guide")
    video = next(v for v in VIDEOS if v["slug"] == "nominees-annuity")
    pay_q = next(q for q, _, _ in guide["qa"] if q.startswith("What does a nominees' annuity pay?"))
    who_q = next(q for q, _, _ in guide["qa"] if q == "Who can be a nominee?")
    guide_live = guide["slug"] in _LIVE_GUIDE_SLUGS
    title = "The nominees' annuity example: what two insurers quoted in August 2026"
    seo_title = f"Nominees' annuity example: the quotations | {SITE_NAME}"
    desc = ("What Just and Canada Life quoted in August 2026 for the nominees' annuity example: £500,000, "
            "lives aged 75 and 45. Expired rates, not a recommendation.")
    doc_sources = ["q_just_doc", "q_cl_doc"]
    further_sources = ["q_just_aug", "just_terms", "q_cl_doc", "q_cl_aug"]
    nominee_sources = ["q_age40", "q_just_sep", "q_cl_sep", "fa2004p15", "fa2004p27A", "fa2004p27AA", "ptm071200"]
    duration_sources = ["q_just_doc", "q_just_aug", "just_terms", "q_cl_doc", "q_cl_aug", "fa2004p27AA", "ptm072200"]
    pub = nice_date(date.fromisoformat(EVIDENCE_PUBLISHED))
    rows = [
        ("Purchase price", "£500,000.00", "£500,000.00"),
        ("Income a year, before tax", "£29,153.64", "£28,925.76"),
        ("Income a month (the yearly income divided by 12)", "£2,429.47", "£2,410.48"),
        ("Annuity rate (the yearly income divided by the price)", "5.83%", "5.79%"),
        ("Income to the second life if the first life dies first", "100%: £29,153.64 a year",
         "100%: £28,925.76 a year"),
        ("Rate guaranteed", "Until 24 August 2026, extended to 24 September 2026 if Just received the "
         "application by 24 August", "If Canada Life received the completed application by 24 August 2026 "
         "and the money by 24 September 2026"),
    ]
    rows_html = "\n".join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td></tr>'
                          for a, b, c in rows)
    if guide_live:
        guide_pay = f'<a href="/{guide["slug"]}/#{slugify(pay_q)}">{esc(pay_q)}</a>'
        guide_who = f' The guide explains <a href="/{guide["slug"]}/#{slugify(who_q)}">who can be a nominee</a>.'
        used_in = (f'The <a href="/{guide["slug"]}/">nominees\' annuity guide</a> and the '
                   f'<a href="/{video["slug"]}/">nominees\' annuity video page</a> use')
        related = (f'<div class="related"><p><strong>Where these figures are used:</strong> the guide answer '
                   f'{guide_pay}, and the <a href="/{video["slug"]}/">nominees\' annuity video page</a>.</p></div>')
    else:
        guide_who = ""
        used_in = f'The <a href="/{video["slug"]}/">nominees\' annuity video page</a> uses'
        related = (f'<div class="related"><p><strong>Where these figures are used:</strong> the '
                   f'<a href="/{video["slug"]}/">nominees\' annuity video page</a>.</p></div>')
    page = {
        "@type": "WebPage",
        "@id": url,
        "url": url,
        "name": title,
        "headline": title,
        "description": desc,
        "inLanguage": "en-GB",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "author": {"@id": f"{SITE}/#steve-hunt"},
        "publisher": {"@id": f"{SITE}/#steve-hunt"},
        "datePublished": EVIDENCE_PUBLISHED,
        "dateModified": EVIDENCE_PUBLISHED,
        "publishingPrinciples": CORRECTIONS_URL,
        "about": [{"@type": "Thing", "name": "Nominees' annuity"}, {"@type": "Thing", "name": "Joint life annuity"}],
        "mentions": [{"@type": "Organization", "name": "Just Retirement Limited"},
                     {"@type": "Organization", "name": "Canada Life Limited"}],
        "citation": [source_ld(k) for k in unique(doc_sources + further_sources + nominee_sources
                                                  + duration_sources)],
    }
    ld = {"@context": "https://schema.org", "@graph": [website_ld(), person_ld(), page]}
    return f"""<!doctype html>
<html lang="en-GB">
<head>
{HEAD_COMMON}<title>{esc(seo_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="{esc(AUTHOR)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_GB">
<style>{CSS}{EVIDENCE_CSS}</style>
{ld_script(ld)}
</head>
<body>
{header_html()}
<main class="wrap">
<article>
<p class="kicker">Provider evidence &middot; Nominees' annuity</p>
<h1>{esc(title)}</h1>
<p class="byline">By <a href="#about-the-author">Steve Hunt ACII TEP</a> &middot; Quotations dated 10 and 11 August 2026 &middot; Extract published {pub}</p>
<p>{used_in} two quotations obtained in August 2026. This page sets out what those two documents say, so that readers can see exactly what the figures rest on. The rates have expired, and nothing here is a recommendation.</p>
<p>These were quotation illustrations for a fictitious example, not records of policies purchased. The Just illustration was supplied by Just itself. The amounts and the guarantee wording below are recorded as historical documentary evidence, not as offers open for acceptance now.</p>

<section class="answer" id="in-short">
<h2>In short</h2>
<p>On 11 August 2026 Just quoted £29,153.64 a year, and on 10 August 2026 Canada Life quoted £28,925.76 a year. Each was for a lifetime annuity on two lives, bought with £500,000 of pension money. The first life was a man aged 75. If he dies first, 100% of the income is then paid to the second life, a woman aged 45. Neither quotation uses the word nominee; that point is explained below. Both rates were guaranteed for a few weeks only, until 24 September 2026 at the latest, and have expired.</p>
</section>

<h2 id="the-quotations">The two quotations</h2>
<div class="tablewrap"><table class="ev">
<caption>Quoted in August 2026. These rates have expired.</caption>
<thead><tr><th scope="col"></th><th scope="col">Just, 11 August 2026</th><th scope="col">Canada Life, 10 August 2026</th></tr></thead>
<tbody>
{rows_html}
</tbody>
</table></div>
<p class="note">The monthly figures and the annuity rates are worked out from the yearly income. Every other figure is as printed on the quotations.</p>
{sources_html(doc_sources)}

<h2 id="terms">What the quotations say</h2>
<ul class="facts">
<li>Product: a lifetime annuity, as both quotations call it, bought with £500,000 from a registered pension scheme. Just's quotation shows no tax-free lump sum taken; Canada Life's does not mention one.</li>
<li>First life: male, aged 75 on the date of the quotation. Second life: female, aged 45. In the guide and the video they are a fictitious father and his daughter.</li>
<li>Level income: it never increases, so its buying power falls as prices rise. Canada Life's quotation warns of this.</li>
<li>Paid monthly in arrears, without proportion: no part payment is made for the days between the last payment and a death.</li>
<li>If the first life dies first, 100% of the income is then paid to the second life. Canada Life's quotation says this starts only after the first life's death. Neither quotation says how long it lasts: see below.</li>
<li>No guarantee period. Canada Life's quotation shows none, and under that heading Just's says only that the income will continue throughout the first life's lifetime.</li>
<li>No value protection on either, and no cash-in or surrender value at any time, so nothing more would be paid once both lives had died. Canada Life's quotation adds that once the cancellation period has passed, the policy cannot be changed in any way.</li>
<li>No adviser charge paid out of the purchase price. Canada Life's quotation shows an adviser charge of £0.00, and Just's says it has not been asked to make any adviser charge payment.</li>
<li>The income is taxable. Both quotations say income tax is normally taken off before the income is paid.</li>
<li>Both quotations say the income could be changed if any of the details given were wrong or changed.</li>
</ul>
<p>Both quotations say they should be read with the insurer's Key Features Document. The quotation alone is not the full contract; the applicable policy conditions and schedule must also be checked. The supporting evidence used for the second life's payment duration is distinguished below.</p>

<h2 id="further-evidence">Further evidence held</h2>
<ul class="facts">
<li>Just: the request for its illustration, sent on 8 August 2026, asked for 100% of the income to continue to the daughter for the rest of her life, and for the standard rate rather than an enhanced one, with both lives in good health. Just supplied the figures on 11 August 2026 as non-underwritten rates on the basis requested, and the same day confirmed that the figure could be published.</li>
<li>Just's published policy conditions say the contract is formed by the application, any medical statements, the policy conditions and the policy schedule (condition 3.1), and that the dependant's income shown in the policy schedule is paid to the surviving dependant "for the remainder of their life" (condition 6.2.1). These are Just's current published conditions, retrieved on 3 October 2026, not a policy schedule issued for this example.</li>
<li>Canada Life: the request for its quotation, sent on 9 August 2026, asked for 100% of the income to continue to the daughter for the rest of her life, and for the standard rate rather than an enhanced one, with both lives in good health. Canada Life supplied the quotation on 10 August 2026 on that request, described the continuing income as a dependant's pension nominated at outset, and the same day confirmed it was happy to be named.</li>
</ul>
{sources_html(further_sources)}

<h2 id="nominee-or-dependant">Nominee or dependant?</h2>
<p>Neither quotation uses the word nominee. Just's quotation calls the second life the dependant, and Canada Life's calls her the second annuitant, with "Dependant's income" in its summary. So the nominee point does not come from these documents. It comes from the pension tax rules and from the insurers' separate answers.</p>
<p>For the annuity and nominee rules discussed here, a member's child aged 23 or over is not a dependant merely because the member supports them financially. Impairment and certain older-scheme protections can change that. The fictitious daughter is assumed to fall outside those exceptions and to be nominated by her father. On those assumptions, a qualifying related annuity for her is a nominees' annuity.</p>
<p>In August 2026 both insurers said they would write a nominees' annuity where the nominee is aged 40 or over. In September 2026 Just told Steve that its documents use the word dependant for both dependants and nominees, and that its application form is the member's binding nomination.{guide_who}</p>
{sources_html(nominee_sources)}

<h2 id="how-long">How long the second life's income lasts</h2>
<p>Neither quotation sheet expressly states how long the second life's income lasts. For the Just example, Steve requested lifetime continuation and Just replied on the requested basis. Just's separately published policy conditions, condition 6.2.1, also provide for the surviving named second life's income for the remainder of that person's life. For the Canada Life example, Steve likewise requested lifetime continuation, and Canada Life quoted on that request. The pension tax rules permit a nominees' annuity to last for life or to end earlier on marriage or civil partnership. That permitted alternative does not establish that either illustration contains such an ending condition.</p>
{sources_html(duration_sources)}

<h2 id="withheld">What this page leaves out, and why</h2>
<ul>
<li>The names and dates of birth on the quotations. The two lives were fictitious, and their ages on the date of the quotation are given instead.</li>
<li>The postcode Canada Life used to price its quotation.</li>
<li>The name and address of the adviser firm that requested Canada Life's quotation.</li>
<li>The intermediary details on Just's quotation. Just produced that quotation itself, so they show one of Just's own accounts, not an adviser firm.</li>
<li>The insurers' reference numbers.</li>
<li>The documents themselves. They are the insurers' documents, so this page describes them rather than reproducing them. The originals are held on file.</li>
</ul>

<h2 id="why-named">Why the insurers are named</h2>
<p>Naming the insurers records where the quotations came from. It is not a recommendation of either insurer or of this kind of annuity. The other insurers asked in August 2026 said no at that time, though some were reviewing, and the market may have changed since.</p>

<h2 id="today">Today's rates</h2>
<p>The quotation guarantees expired by 24 September 2026. These are historical illustrations, not current offers. A new quotation would need to be obtained; its income and terms could differ according to the rates and case details at that time. Canada Life's quotation points readers to MoneyHelper, the free guidance service backed by government, to compare annuities from different insurers: <a href="https://www.moneyhelper.org.uk/en/pensions-and-retirement/taking-your-pension/compare-annuities" target="_blank" rel="noopener">MoneyHelper: Compare annuities</a>.</p>

{related}

{author_box()}
<p class="disclaimer">This page is education only. It records dated quotations that have expired. It is not advice, not a personal recommendation, and not an invitation to do business, and nothing here takes account of your circumstances.</p>
</article>
</main>
{footer_html()}
</body>
</html>
"""


def not_found_page():
    return f"""<!doctype html>
<html lang="en-GB">
<head>
{HEAD_BASE}<meta name="robots" content="noindex">
<title>Page not found | {esc(SITE_NAME)}</title>
<style>{CSS}</style>
</head>
<body>
{header_html()}
<main class="wrap">
<h1>That page is not here</h1>
<p>Try the <a href="/">home page</a>, which lists every video with its transcript.</p>
</main>
{footer_html()}
</body>
</html>
"""


def sitemap():
    urls = ([(SITE + "/", TODAY.isoformat())]
            + [(f"{SITE}/{v['slug']}/", v["modified"]) for v in VIDEOS]
            + [(f"{SITE}/{g['slug']}/", g["modified"]) for g in GUIDES]
            + [(ABOUT_URL, TODAY.isoformat())]
            + ([(EVIDENCE_URL, EVIDENCE_PUBLISHED)] if INCLUDE_EVIDENCE else [])
            + [(CORRECTIONS_URL, TODAY.isoformat())])
    body = "\n".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'


def robots():
    return (
        "# Inheritance Tax Explained, by Steve Hunt ACII TEP.\n"
        "# Everything on this site is public education. All crawlers are welcome, including AI assistants.\n"
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {SITE}/sitemap.xml\n"
    )


def llms_txt():
    lines = [
        f"# {SITE_NAME}",
        "",
        f"> {website_ld()['description']}",
        "",
        "Author: Steve Hunt ACII TEP, Chartered Insurance Risk Manager and Trust and Estate Practitioner, in UK financial services since 1980.",
        f"About the author: {ABOUT_URL}",
        f"LinkedIn: {LINKEDIN}",
        f"YouTube: {YOUTUBE_CHANNEL}",
        f"X: {X_PROFILE}",
        "",
        "## Videos with key facts, sources and full transcripts",
        "",
    ]
    for v in VIDEOS:
        lines.append(f"- [{v['title']}]({SITE}/{v['slug']}/): {v['short_answer'][0]}")
    lines += ["", "## Guides: one subject, every question answered, with sources", ""]
    for g in GUIDES:
        lines.append(f"- [{g['title']}]({SITE}/{g['slug']}/): {g['short_answer'][0]}")
    lines += [
        "",
        "## Sources and corrections",
        "",
        f"- [Sources, method and corrections]({CORRECTIONS_URL}): every answer links to the law on legislation.gov.uk "
        "and to HMRC guidance on GOV.UK, and each source is labelled " + ", ".join(LABEL_ORDER[:-1]) + " or "
        + LABEL_ORDER[-1] + ". Transcripts are not edited; dated notes sit beside any correction.",
        f"- [About Steve Hunt ACII TEP]({ABOUT_URL}): who writes these answers, his qualifications and experience, "
        "and his LinkedIn articles.",
    ] + ([
        f"- [The nominees' annuity example: what two insurers quoted in August 2026]({EVIDENCE_URL}): the figures "
        "and terms in the Just and Canada Life quotations, and what was withheld. Dated evidence; the rates have expired.",
    ] if INCLUDE_EVIDENCE else []) + [
        "",
        "## Notes",
        "",
        "Education only. Not advice, not a personal recommendation, and not an invitation to do business. "
        "Last reviewed " + AS_AT + ".",
    ]
    return "\n".join(lines) + "\n"


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    import shutil
    shutil.rmtree(OUT, ignore_errors=True)  # start clean so no draft page is ever left behind in out/
    for k in SOURCES:
        assert SOURCES[k][0] in LABEL_ORDER, k
    write("index.html", home_page())
    for v in VIDEOS:
        for _, ks in v["key_facts"]:
            for k in ks:
                assert k in SOURCES, k
        for _, _, ks in v["faq"]:
            for k in ks:
                assert k in SOURCES, k
        write(f"{v['slug']}/index.html", video_page(v))
    for g in GUIDES:
        for _, _, ks in g["qa"]:
            for k in ks:
                assert k in SOURCES, k
        write(f"{g['slug']}/index.html", guide_page(g))
    write(f"{CORRECTIONS_SLUG}/index.html", corrections_page())
    write(f"{ABOUT_SLUG}/index.html", about_page())
    if INCLUDE_EVIDENCE:
        write(f"{EVIDENCE_SLUG}/index.html", evidence_page())
    write("404.html", not_found_page())
    write("sitemap.xml", sitemap())
    write("robots.txt", robots())
    write("llms.txt", llms_txt())
    import shutil
    os.makedirs(os.path.join(OUT, "images"), exist_ok=True)
    for fn in os.listdir(os.path.join(HERE, "static", "images")):
        shutil.copy(os.path.join(HERE, "static", "images", fn), os.path.join(OUT, "images", fn))
    # sanity checks
    for root, _, files in os.walk(OUT):
        for fn in files:
            if not fn.endswith((".html", ".txt", ".xml")):
                continue
            p = os.path.join(root, fn)
            txt = open(p, encoding="utf-8").read()
            assert "—" not in txt and "–" not in txt, f"dash in {p}"
    print("built", OUT)


if __name__ == "__main__":
    main()
