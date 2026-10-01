#!/usr/bin/env python3
"""Builds the Inheritance Tax Explained static site (Steve Hunt ACII TEP).

Output goes to site/out/. Every page is self-contained HTML with inline CSS,
plain semantic markup and JSON-LD, so that search engines and AI crawlers can
read the whole thing without running any JavaScript.
"""
import html
import json
import os
import re
from datetime import date

SITE = "https://inheritancetaxexplained.co.uk"
SITE_NAME = "Inheritance Tax Explained"
AUTHOR = "Steve Hunt ACII TEP"
LINKEDIN = "https://www.linkedin.com/in/steve~hunt"
YOUTUBE_CHANNEL = "https://www.youtube.com/@SteveHuntACIITEP"
PLAYLIST = "https://www.youtube.com/playlist?list=PLYeD4F-FZfOA"
TODAY = date(2026, 10, 1)
AS_AT = "September 2026"
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
# Video data
# ---------------------------------------------------------------------------

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
            "From 6 April 2027, unused pension funds come within the scope of UK inheritance tax "
            "for the first time. What changes, which pensions are excluded, and how a £500,000 "
            "pension could cost a family £516,000 in tax. Video, key facts and full transcript "
            "by Steve Hunt ACII TEP."
        ),
        "published": "2026-09-29",
        "seconds": 647,
        "duration_iso": "PT10M47S",
        "duration_text": "10 min 47 sec",
        "short_answer": [
            "From 6 April 2027, most unused pension funds and pension death benefits count as part of "
            "your estate for inheritance tax, and can be taxed at 40% on death. Pensions left to a "
            "spouse or civil partner stay exempt. Unmarried partners are not covered.",
            "Three kinds of pension are excluded: dependants' pensions from a defined benefit scheme, "
            "death in service benefits, and joint life annuities bought in your lifetime, including the "
            "nominees' annuity.",
            "If your estate with the pension is under the nil rate bands, there is no inheritance tax at "
            "all. In a severe case, with a large estate and a beneficiary who is a higher earner, a "
            "£500,000 pension could cost a family £516,000 in inheritance tax and income tax combined. "
            "Most families will pay far less, and some nothing.",
        ],
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
            "From 6 April 2027, most unused pension funds and pension death benefits count as part of the "
            "estate for inheritance tax: Inheritance Tax Act 1984, s.150A, inserted by Finance Act 2026, "
            "s.66, for deaths on or after 6 April 2027.",
            "Pensions left to a spouse or civil partner remain exempt (Inheritance Tax Act 1984, s.18). "
            "Unmarried partners are not covered.",
            "Excluded: dependants' scheme pensions, death in service benefits, and dependants' or nominees' "
            "annuities bought together with the member's own annuity. Annuity guarantee periods and value "
            "protection are included.",
            "The residence nil rate band reduces by £1 for every £2 that an estate is over £2 million "
            "(Inheritance Tax Act 1984, s.8D).",
            "If death is at 75 or over, the person who inherits the pension also pays income tax on what "
            "they draw.",
            "Business property relief, agricultural property relief and the ten-year instalment option do "
            "not apply to pension funds. The tax is due by the end of the sixth month after the month of "
            "death.",
            "The worked example is a severe case. Most families will pay far less, and some nothing at all.",
        ],
        "assumptions": (
            "Assumptions in the worked example: 2026/27 rates and allowances, frozen; no fund growth; "
            "Mr Miggins died under 75 and before 6 April 2027; Mrs Miggins dies in 2029 aged over 75; "
            "her estate without the pension is £2 million; Amy earns £100,000 a year; English income "
            "tax rates. Mr and Mrs Miggins are fictitious. The arithmetic is not."
        ),
        "faq": [
            ("What changes to pensions and inheritance tax on 6 April 2027?",
             "From 6 April 2027, unused pension money from personal pensions, SIPPs and money purchase "
             "company pension schemes becomes part of your estate for inheritance tax, and can be taxed at "
             "40% on your death. The change is made by section 150A of the Inheritance Tax Act 1984, "
             "inserted by the Finance Act 2026. Spouse and civil partner exemptions still apply. Common law "
             "partners are not covered."),
            ("Which pensions are excluded from inheritance tax from April 2027?",
             "Three main categories: widows', widowers' and other dependants' pensions from a defined "
             "benefit (final salary or average salary) scheme; death in service benefits; and joint life "
             "annuities bought in the member's lifetime, including the nominees' annuity. Annuity guarantee "
             "periods and value protection are not excluded. They count as part of the estate."),
            ("Can inheritance tax on a £500,000 pension really cost more than the pension itself?",
             "In a severe case, yes. In the worked example, Mrs Miggins inherited a £500,000 pension from "
             "her husband, who died before 75, so it could all have been paid out tax free. Because her own "
             "estate was already £2 million, adding the pension cost £300,000 in inheritance tax at an "
             "effective 60%. Because she died over 75, her daughter Amy then paid income tax on what she "
             "drew, also at an effective 60% because of the personal allowance taper, adding £216,000 over "
             "15 years. Total: £516,000, which is £16,000 more than the pension was worth."),
            ("Why is the pension taxed at 60% in the example rather than 40%?",
             "The residence nil rate band is reduced by £1 for every £2 that an estate is over £2 million "
             "(Inheritance Tax Act 1984, s.8D). Adding a £500,000 pension to a £2 million estate loses the "
             "residence nil rate band on top of the 40% charge. The effect is an additional £300,000 of "
             "tax on the £500,000 pension, which is an effective rate of 60%."),
            ("Does the pension fund pay the inheritance tax it causes?",
             "No. The pension pays its proportionate share of the whole estate's bill, not the tax it "
             "triggers. In the example the pension is one fifth of a £2.5 million estate. The total tax is "
             "£700,000, so the pension pays £140,000, leaving £360,000 in the pension, which Amy then draws "
             "as taxable income."),
            ("Can business property relief, agricultural property relief or the ten-year instalment option apply to pension funds?",
             "No. The government's technical note says that you are not treated as owning the pension's "
             "assets, and uses that sentence to refuse business property relief, agricultural property "
             "relief, loss on sale relief and the ten-year instalment option. The tax on the pension must "
             "be settled by the end of the sixth month after the month of death, with interest running "
             "after that."),
            ("How will your pension be taxed when you die after April 2027?",
             "Your pension fund will form part of your estate on death, unless it goes to a spouse or civil "
             "partner or is one of the excluded types. If your estate with the pension is under the nil "
             "rate bands, £325,000 plus up to £175,000 for your home, each, up to £1 million for a married "
             "couple, it pays no inheritance tax at all. Above that, the rate is 40%, rising to an "
             "effective 60% where the residence nil rate band tapers away, plus income tax for the person "
             "who inherits if you die at 75 or over."),
        ],
        "articles": [
            ("husband", "The worked example, Mrs Miggins and her daughter Amy."),
            ("oneword", "The word \"notional\", and the one clause that takes a pension back out of the net."),
        ],
        "related": [("Next video", "nominees-annuity",
                     "Nominees' annuity: what is it, how does it work, and what's the catch?")],
        "legislation": "Inheritance Tax Act 1984, s.18, s.8D and s.150A(1), inserted by Finance Act 2026, s.66.",
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
            "A nominees' annuity is a joint life annuity where the second life is a child, grandchild or "
            "anyone else you nominate. How it works, with two real quotations, and the catches, including "
            "whether buying one is a gift. Video, key facts and full transcript by Steve Hunt ACII TEP."
        ),
        "published": "2026-09-29",
        "seconds": 919,
        "duration_iso": "PT15M19S",
        "duration_text": "15 min 19 sec",
        "short_answer": [
            "A nominees' annuity is a joint life annuity where the second life is a child, grandchild or "
            "anyone else you nominate, rather than a spouse or civil partner. It is bought by the pension "
            "member, in the member's lifetime, together with the member's own lifetime annuity. When the "
            "member dies, the income carries on to the nominee for the rest of their life.",
            "Bought that way, it is excluded from the member's estate for inheritance tax from 6 April "
            "2027. On a real quotation from August 2026, a £500,000 pension fund was offered a joint life "
            "annuity of £29,153.64 a year for a father of 75, with 100% continuation to his daughter of 45.",
            "The catches: only the member can set it up, and only while alive; it is normally bought with "
            "no guarantee period and no value protection; insurers currently want the nominee to be at "
            "least 40; and whether the purchase counts as a lifetime gift for inheritance tax is not yet "
            "settled.",
        ],
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
            "Legal definition: Finance Act 2004, Schedule 28, paragraph 27AA(1), inserted by Finance Act 2015. "
            "A nominee must not be a dependant under the pension tax rules (paragraph 27A).",
            "From 6 April 2027, a nominees' annuity bought together with the member's own lifetime annuity is "
            "excluded from the estate for inheritance tax: Inheritance Tax Act 1984, s.150A(6)(c), inserted "
            "by Finance Act 2026, for deaths on or after 6 April 2027. Nominees' annuities bought after the "
            "member's death are also allowed, but that is not the route that qualifies for this exclusion.",
            "Remaining guarantee payments and value protection death benefits come within inheritance tax "
            "from 6 April 2027. The example in the video leaves both out.",
            "The quotations: Just, 11 August 2026, 5.83%, £29,153.64 a year. Canada Life, 10 August 2026, "
            "5.79%, £28,925.76 a year. Both on £500,000, parent 75, nominee 45, level, no guarantee, no value "
            "protection, monthly in arrears, 100% continuation, standard rates, no adviser charge.",
            "Age 40 or over, including age 40, is a provider condition (Just and Canada Life, August 2026), "
            "not a legal minimum.",
            "Whether buying one is a gift for inheritance tax is not settled. The £50,000 in Bill's example is "
            "an assumed value for illustration: halving the income does not by itself set the tax value. The "
            "£20,000 assumes death within 3 years and no nil rate band or exemptions available. Taper relief "
            "reduces the tax after 3 years.",
            "Whole of life cover continues beyond 7 years, and term cover can cover the 7-year risk. Premiums "
            "must be maintained and claim conditions met, and total premiums can exceed the payout.",
            "The annuity income is taxable. Salary sacrifice means Amy gives up salary in return for employer "
            "pension contributions; the annuity itself stays taxable, and any saving depends on her "
            "circumstances and pension limits. From 6 April 2029, the National Insurance exemption is limited "
            "to £2,000 a year of pension salary sacrifice.",
            "A level income loses buying power with inflation, and the purchase normally cannot be reversed "
            "after the cancellation period.",
        ],
        "assumptions": (
            "Mr Miggins, his brother Bill, and Amy are fictitious. The quotations are real, obtained in "
            "August 2026 for a LinkedIn article, and will have changed since."
        ),
        "faq": [
            ("What is a nominees' annuity?",
             "A nominees' annuity is a joint life annuity where, instead of the second life being a spouse, "
             "civil partner or common law partner, the second life is a child or grandchild, or anyone else "
             "that the pension member nominates. It came out of George Osborne's 2015 pension freedoms and "
             "has been available for over a decade, but insurers have only recently started to write them."),
            ("What is the legal definition of a nominees' annuity?",
             "Finance Act 2004, Schedule 28, paragraph 27AA(1), inserted by the Finance Act 2015. An annuity "
             "payable to a nominee is a nominees' annuity if either it is purchased together with a lifetime "
             "annuity payable to the member, and the member becomes entitled to that lifetime annuity on or "
             "after 6 April 2015; or it is purchased after the member's death, the member dies on or after "
             "3 December 2014, and the nominee becomes entitled to the annuity on or after 6 April 2015. "
             "Only the first route, bought together with the member's own annuity, is excluded from "
             "inheritance tax under section 150A(6)(c) of the Inheritance Tax Act 1984."),
            ("Why is the nominees' annuity in the Finance Act 2004 if it came from the 2015 pension freedoms?",
             "Because the Finance Act 2015 inserted the new wording into the Finance Act 2004, which is the "
             "Act that holds the pension tax rules. So it appears in the 2004 Act, but it did not exist "
             "until the 2015 Act put it there."),
            ("How does a nominees' annuity work in practice?",
             "Take a father of 75 with a £500,000 pension fund and a daughter of 45. On real quotations from "
             "August 2026, Just offered £29,153.64 a year (£2,429.47 a month) at 5.83%, and Canada Life "
             "£28,925.76 a year at 5.79%. Both were level, with no guarantee period, no value protection, "
             "paid monthly in arrears, with 100% continuation to the daughter for the rest of her life. When "
             "the father dies, the same monthly income carries on to her. Bought together with his own "
             "annuity, it is excluded from his estate for inheritance tax."),
            ("What is the catch with a nominees' annuity?",
             "It can only be set up by the pension member, and only while the member is alive, because the "
             "law says it must be purchased together with a lifetime annuity payable to the member. The "
             "option dies with the member: a widow who inherits her husband's pension cannot buy one with "
             "it. It is normally bought with no guarantee and no value protection, because both of those "
             "would count for inheritance tax. Insurers currently want the nominee to be at least 40, which "
             "is a provider condition rather than a legal one. And whether buying one is a lifetime gift for "
             "inheritance tax has not been settled."),
            ("Is buying a nominees' annuity a gift for inheritance tax?",
             "Nobody has settled it yet. The logic of the argument: if a £100,000 pot would buy a single "
             "life annuity of £10,000 a year, and the member takes £5,000 a year instead so that 100% "
             "continues to his son, he has given away half his pension income. If the same proportion is "
             "applied to the pot, that could be treated as a gift of £50,000, a potentially exempt transfer. "
             "If he lives seven years, nothing is taxed. If he dies within seven years, the failed gift "
             "could be counted against his estate, up to £20,000 of tax at 40% in the worst case. Steve's "
             "reading of the law as written: buy one before 6 April 2027 and it may be a gift; buy one after "
             "6 April 2027 out of a pension trust and it may not be a gift at all. The full argument is in "
             "his article Osborne's Get Out of Jail Card Under Attack."),
            ("How can the seven-year gift risk be covered?",
             "With a whole of life assurance plan, written in trust. It pays out exactly when the gift "
             "fails, which is on death within seven years, so it is the hedge. Whole of life is assurance "
             "rather than insurance: it pays on an event that will happen, the only unknown being when. "
             "There is one more risk, both lives ending early. If the nominee were to die soon after the "
             "member, the continuation dies with them, so the nominee can take out a ten-year term policy "
             "on their own life, in trust. Premiums must be kept up and claim conditions met, and total "
             "premiums can exceed the payout."),
            ("Is the income from a nominees' annuity taxable?",
             "Yes. The income to the nominee is taxable as income. A nominee who is employed may be able to "
             "get some or all of that tax back by paying more into their own pension through salary "
             "sacrifice, but the annuity itself stays taxable, and any saving depends on their "
             "circumstances and pension limits. From 6 April 2029, the National Insurance exemption is "
             "limited to £2,000 a year of pension salary sacrifice."),
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
        "legislation": "Finance Act 2004, Schedule 28, paragraphs 27A and 27AA(1), inserted by Finance Act 2015; "
                       "Inheritance Tax Act 1984, s.150A(6)(c), inserted by Finance Act 2026.",
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
            "Whole of life assurance pays a fixed sum when you die, whenever that is. What it is, why the "
            "unit-linked plans of the 1980s made a generation distrust it, and what has changed: guaranteed "
            "premiums and a real quotation showing generational wealth transfer. Video, key facts and full "
            "transcript by Steve Hunt ACII TEP."
        ),
        "published": "2026-10-01",
        "seconds": 783,
        "duration_iso": "PT13M3S",
        "duration_text": "13 min 3 sec",
        "short_answer": [
            "Whole of life assurance puts a monetary value on a person's life, the sum assured, and pays it out "
            "when that person dies, whenever that is, provided the premiums are paid. Since the Life Assurance "
            "Act 1774 you can only insure a life in which you have an insurable interest, and an individual has "
            "an unlimited insurable interest in their own life and in the life of their spouse or civil partner.",
            "A whole generation distrusts it because of the unit-linked whole of life plans of the 1980s, sold "
            "by the hundreds of thousands by companies like Abbey Life and Allied Dunbar: reviewable premiums, "
            "cover that could be cut, policies that lapsed with nothing to show for years of premiums, and "
            "payouts that sometimes fell short of the premiums paid in.",
            "What has changed: conventional whole of life is whole of life again, with a premium guaranteed from "
            "day one. On a real quotation, a man of 75 pays £1,555.20 a month for £500,000 written in trust. Die "
            "at 80 and the trust receives £500,000 for £93,312 of premiums. The same £93,312 left in his estate "
            "would leave his family £55,987 after 40% inheritance tax, or as little as £37,325 at an effective "
            "60%. Total premiums only pass the sum assured if he lives to nearly 102. The catch is that age and "
            "health decide the premium, and whether cover is offered at all.",
        ],
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
            "Whole of life assurance puts a monetary value on a life, the sum assured, and pays it when that "
            "person dies, whenever that is, provided the premiums are paid. On a conventional plan the premium "
            "is guaranteed from day one and is never reviewed.",
            "Life Assurance Act 1774, also known as the Gambling Act: a policy on someone's life is void unless "
            "the person taking it out has an insurable interest in that life (section 1), and the amount "
            "recoverable is limited to the value of that interest (section 3). An individual has an unlimited "
            "insurable interest in their own life and in the life of their spouse or civil partner. Beyond that "
            "the only limits are the insurer accepting the risk and the premiums being affordable.",
            "The unit-linked whole of life plans of the 1980s were investment policies with a death benefit "
            "attached. Premiums were reviewable: to keep the same cover the premium could go up, or the cover "
            "could be cut, and some policies lapsed with nothing to show for years of premiums. The new rules on "
            "selling investments came in under the Financial Services Act 1986, in force from April 1988.",
            "The quotation in the video: a man of 75, £500,000 of conventional whole of life assurance, written "
            "in trust, guaranteed premium £1,555.20 a month, £18,662.40 a year.",
            "Premiums paid against the £500,000 paid to the trust: death at 80, £93,312; at 85, £186,624; at 90, "
            "£279,936; at 95, £373,248; at 100, £466,560. Total premiums only pass the sum assured if he lives "
            "to nearly 102.",
            "Keep that money in the estate instead and the £93,312 he would have paid by 80 is taxed at 40%, "
            "leaving £55,987. If it tips the estate over £2 million, the residence nil rate band is reduced by £1 "
            "for every £2 over (Inheritance Tax Act 1984, s.8D), an effective 60%, leaving £37,325.",
            "Written in trust, the sum assured is paid to the trustees and does not form part of the estate. "
            "Premiums paid for a policy held in trust are gifts, usually covered by the normal expenditure out "
            "of income exemption (Inheritance Tax Act 1984, s.21) or the £3,000 annual exemption (s.19).",
            "Term insurance, like car or house insurance, is a cost if it does not pay out. Whole of life "
            "assurance pays out on an event that is certain to happen; the only unknown is when. The premiums "
            "must be paid for life: stop the premiums and the cover stops.",
            "Age and health decide the premium, and whether cover is offered at all, and neither stays still. "
            "Cover available today may not be available after a scan or a blood test tomorrow.",
            "James Dodson, who worked out the level premium system still used to price whole of life assurance, "
            "was refused cover by the Amicable Society for being over 45. He died in 1757, before the Equitable "
            "Society he had planned opened in 1762, leaving three children unprovided for.",
        ],
        "assumptions": (
            "Mr Miggins is fictitious. The quotation is real, obtained in 2026; premiums depend on age, health "
            "and the insurer, and will differ on the day. The 60% figure applies where an estate sits between "
            "£2 million and £2.7 million and the residence nil rate band taper applies. Figures are rounded to "
            "the pound."
        ),
        "faq": [
            ("What is whole of life assurance?",
             "Whole of life assurance puts a monetary value on a person's life, for example £500,000, which is "
             "called the sum assured. When that person dies, the insurance company pays the sum assured, "
             "whenever death occurs, provided the premiums have been paid. In its basic, traditional form it "
             "is as simple as that, and it has worked that way since the Life Assurance Act 1774."),
            ("What is insurable interest?",
             "Before 1774 it was common for the rich to take out life assurance on complete strangers, and even "
             "on kings and queens, in the coffee houses of London. It was a form of gambling, which is why the "
             "Life Assurance Act 1774 was also known as the Gambling Act. The Act says you cannot take out a "
             "life assurance policy on someone unless you have an insurable interest in that person, meaning "
             "you would suffer a financial loss if they died. An individual has an unlimited insurable interest "
             "in their own life and in the life of their spouse or civil partner, so a husband could insure his "
             "wife for £10 million or £100 million. The only limits are an insurer accepting the risk and the "
             "premiums being paid."),
            ("Why does a whole generation distrust whole of life assurance?",
             "For 200 years whole of life assurance did exactly what it was designed to do: pay a lump sum on "
             "death, often used to cover death duties. Then the unit-linked companies of the 1960s to 1980s, "
             "Abbey Life, Hambro Life and later Allied Dunbar among them, brought in the unit-linked whole of "
             "life policy, an investment with a death benefit attached. Premiums could be reviewed, cover could "
             "be cut, some policies lapsed with nothing to show for years of premiums, and on death the sum "
             "assured sometimes fell short of the premiums paid in. They were sold by the hundreds of thousands "
             "in the wild west before the new rules on selling investments arrived in 1988. Boomers watched the "
             "foot-in-the-door salesman and the mis-selling in real time, and many vowed never to be caught "
             "again."),
            ("What has changed with whole of life assurance?",
             "Today, conventional whole of life assurance is whole of life again: a premium guaranteed from day "
             "one, and a payout whenever death occurs, provided the premiums are paid. There are no premium "
             "reviews and the cover is not cut. That is why it can be described as generational wealth "
             "transfer rather than insurance."),
            ("How can whole of life assurance be generational wealth transfer?",
             "Take a real quotation for a man of 75: £500,000 of whole of life assurance, written in trust, at "
             "a guaranteed premium of £1,555.20 a month, £18,662.40 a year. If he dies at 80 he has paid "
             "£93,312 in premiums and the trust receives £500,000. At 85, £186,624 paid, £500,000 received. At "
             "90, £279,936. At 95, £373,248. At 100, £466,560. In every case the trust receives £500,000. Total "
             "premiums only pass the sum assured if he lives to nearly 102. The premiums he pays today buy "
             "£500,000 for the next generation tomorrow, and if he dies young the trust gets considerably more "
             "than he paid in."),
            ("What happens if the premium money stays in the estate instead?",
             "Left in his estate, the money is taxed at 40% inheritance tax, or an effective 60% if the estate "
             "sits in the band between £2 million and £2.7 million where the residence nil rate band is "
             "tapered away. Die at 80 and the £93,312 he would have paid in premiums leaves his family £55,987 "
             "after 40% tax, or as little as £37,325 at 60%. Use the same money for premiums on a whole of life "
             "plan in trust and the family trust receives £500,000."),
            ("Is whole of life assurance just a cost, like car insurance?",
             "No. Car insurance, house insurance and term insurance are a cost if they do not pay out, and most "
             "people with term insurance do not die during the term. Whole of life assurance is different: it "
             "pays out on an event that is certain to happen, so the premiums are not lost. The trust gets back "
             "more than is paid in unless the life assured lives to nearly 102. The premiums must be paid for "
             "life, though: stop the premiums and the cover stops."),
            ("Can anyone get whole of life assurance?",
             "No. There are two whens: when the insurer will pay out if you have a policy, and how long cover "
             "will remain available to you. To get whole of life assurance the insurer looks at your age and "
             "your health, decides the premium, and decides whether to offer cover at all. Neither age nor "
             "health stands still, and a future scan that is not clear, or a blood test that needs follow-up, "
             "could mean this type of cover is no longer available."),
            ("Who was James Dodson?",
             "James Dodson was the mathematician who worked out the level premium system, the way whole of "
             "life assurance is still priced today. He was refused cover by the Amicable Society for being over "
             "45, and he died in 1757, before the Equitable Society he had planned opened its doors in 1762, "
             "leaving three children unprovided for. Steve has written about him, and the pastor whose "
             "mortality tables started it all, in his LinkedIn article The Pastor Who Tried to Prove God and "
             "Accidentally Predicted Death."),
        ],
        "articles": [
            ("certainties", "How whole of life was hijacked in the 1980s, and Certainty³: guaranteed income funding guaranteed premiums."),
            ("days86", "The history: Abbey Life, Hambro Life and the first era of mis-selling."),
            ("pastor", "James Dodson, the Amicable Society and the level premium."),
        ],
        "related": [("Previous video", "nominees-annuity",
                     "Nominees' annuity: what is it, how does it work, and what's the catch?")],
        "legislation": "Life Assurance Act 1774, ss.1 to 3; Inheritance Tax Act 1984, s.8D, s.19 and s.21; "
                       "Financial Services Act 1986.",
        "transcript_file": "v3_transcript.tsv",
        "keywords": ["whole of life assurance", "whole of life insurance", "whole of life policy",
                     "generational wealth transfer", "life assurance in trust", "unit-linked whole of life",
                     "Life Assurance Act 1774", "insurable interest", "guaranteed premiums", "inheritance tax"],
    },
]

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


# ---------------------------------------------------------------------------
# CSS (shared, inlined into every page)
# ---------------------------------------------------------------------------

CSS = """
:root{--navy:#0C192B;--navy2:#182C46;--gold:#C8A564;--ivory:#F3EBDA;--paper:#FFFDF8;--ink:#1B2433;--muted:#5A6577;--rule:#E3DCCB;--link:#0F4C81}
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
ul.facts li{margin:.6em 0}
.faq h3{margin-top:1.4em}
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
"""

HEAD_COMMON = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caladea:wght@400;700&display=swap" rel="stylesheet">
"""


def header_html(prefix=""):
    home = prefix if prefix else "./"
    return f"""<header class="site"><div class="wrap">
<a class="brand" href="{home}">{esc(SITE_NAME)} <span>by Steve Hunt ACII TEP</span></a>
<nav><a href="{home}">Home</a><a href="{prefix}pensions-and-inheritance-tax-from-april-2027/">Pensions and IHT 2027</a><a href="{prefix}nominees-annuity/">Nominees' annuity</a><a href="{prefix}whole-of-life-assurance/">Whole of life</a></nav>
</div></header>"""


def footer_html():
    return f"""<footer class="site"><div class="wrap">
<p>{esc(SITE_NAME)}. Plain English explanations of UK inheritance tax by Steve Hunt ACII TEP.</p>
<p>Education only. Not advice, not a personal recommendation, and not an invitation to do business. Tax rules change; check the date on each page.</p>
<p><a href="{LINKEDIN}" rel="me">Steve Hunt on LinkedIn</a> &middot; <a href="{YOUTUBE_CHANNEL}" rel="me">YouTube channel</a> &middot; &copy; 2026 Stephen Hunt</p>
</div></footer>"""


def author_box():
    return f"""<section class="author" id="about-the-author">
<div>
<h2>About Steve Hunt ACII TEP</h2>
<p>Steve Hunt is a Chartered Insurance Risk Manager, an Associate of the Chartered Insurance Institute (ACII), and a Trust and Estate Practitioner (TEP), a full member of STEP. He has worked in UK financial services since 1980, in pensions, protection and estate planning. He writes about inheritance tax, the April 2027 pension changes, annuities, whole of life assurance and trusts.</p>
<p><a href="{LINKEDIN}" rel="me">LinkedIn profile and articles</a> &middot; <a href="{YOUTUBE_CHANNEL}" rel="me">YouTube channel</a></p>
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
        "description": "UK financial services professional since 1980. Chartered Insurance Risk Manager (ACII) and Trust and Estate Practitioner (TEP). Writes and presents plain English explanations of inheritance tax, the April 2027 pension changes, annuities, whole of life assurance and trusts.",
        "url": SITE + "/",
        "sameAs": [LINKEDIN, YOUTUBE_CHANNEL],
        "knowsAbout": ["Inheritance tax", "Pensions and inheritance tax from April 2027", "Nominees' annuities",
                       "Joint life annuities", "Whole of life assurance", "Trusts and estate planning"],
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "name": "ACII, Associate of the Chartered Insurance Institute"},
            {"@type": "EducationalOccupationalCredential", "name": "TEP, Trust and Estate Practitioner (STEP)"},
        ],
    }


def website_ld():
    return {
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "url": SITE + "/",
        "name": SITE_NAME,
        "description": "Plain English explanations of UK inheritance tax, the April 2027 pension changes, annuities, whole of life assurance and trusts, with videos, key facts and full transcripts. By Steve Hunt ACII TEP. Education only.",
        "inLanguage": "en-GB",
        "author": {"@id": f"{SITE}/#steve-hunt"},
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
        "uploadDate": v["published"],
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
    }
    faq = {
        "@type": "FAQPage",
        "@id": f"{url}#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in v["faq"]
        ],
    }
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
        "dateModified": TODAY.isoformat(),
        "video": {"@id": f"{url}#video"},
        "mainEntity": {"@id": f"{url}#video"},
        "learningResourceType": "Concept overview",
        "about": [{"@type": "Thing", "name": k} for k in v["keywords"][:4]],
        "citation": [{"@type": "CreativeWork", "name": ARTICLES[k][0], "url": ARTICLES[k][1], "author": {"@id": f"{SITE}/#steve-hunt"}} for k, _ in v["articles"]],
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

def video_page(v):
    url = f"{SITE}/{v['slug']}/"
    thumb = f"{SITE}/images/{v['slug']}.jpg"
    pub_text = date.fromisoformat(v["published"]).strftime("%-d %B %Y")

    chapters_html = "\n".join(
        f'<li><a class="t" href="{yt_watch(v["id"], s) if s else yt_watch(v["id"])}" target="_blank" rel="noopener">{mmss(s)}</a> '
        f'<a href="#t{s}">{esc(n)}</a></li>'
        for s, n in v["chapters"]
    )
    facts_html = "\n".join(f"<li>{esc(f)}</li>" for f in v["key_facts"])
    faq_html = "\n".join(f"<h3>{esc(q)}</h3>\n<p>{esc(a)}</p>" for q, a in v["faq"])
    articles_html = "\n".join(
        f'<li><a href="{ARTICLES[k][1]}" target="_blank" rel="noopener">{esc(ARTICLES[k][0])}</a> {esc(note)}</li>'
        for k, note in v["articles"]
    )
    sections = transcript_sections(v)
    transcript_html = []
    for start, name, paras in sections:
        link = yt_watch(v["id"], start) if start else yt_watch(v["id"])
        transcript_html.append(
            f'<h3 id="t{start}"><a class="t" href="{link}" target="_blank" rel="noopener">{mmss(start)}</a>{esc(name)}</h3>'
        )
        transcript_html.extend(f"<p>{esc(p)}</p>" for p in paras)
    transcript_html = "\n".join(transcript_html)
    related_html = "".join(
        f'<p><strong>{esc(label)}:</strong> <a href="../{slug}/">{esc(title)}</a></p>'
        for label, slug, title in v["related"]
    )

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
{header_html("../")}
<main class="wrap">
<article>
<p class="kicker">Video {v['number']} &middot; Inheritance tax explained</p>
<h1>{esc(v['title'])}</h1>
<p class="byline">By <a href="#about-the-author">Steve Hunt ACII TEP</a> &middot; Published {pub_text} &middot; Video {v['duration_text']} &middot; Correct as at {AS_AT} &middot; Full transcript below</p>

<section class="answer" id="short-answer">
<h2>The short answer</h2>
{''.join(f'<p>{esc(p)}</p>' for p in v['short_answer'])}
</section>

<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{v['id']}?rel=0" title="{esc(v['title'])}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>
<p class="watch"><a href="{yt_watch(v['id'])}" target="_blank" rel="noopener">Watch on YouTube</a> &middot; <a href="{PLAYLIST}" target="_blank" rel="noopener">All videos in the series</a></p>

<h2 id="chapters">In this video</h2>
<ol class="chapters">
{chapters_html}
</ol>

<h2 id="key-facts">Key facts (as at {AS_AT})</h2>
<ul class="facts">
{facts_html}
</ul>
<p class="note">{esc(v['assumptions'])}</p>
<p class="note">Legislation referred to: {esc(v['legislation'])}</p>

<section class="faq" id="questions">
<h2>Questions this video answers</h2>
{faq_html}
</section>

<h2 id="articles">Steve's LinkedIn articles behind this video</h2>
<ul>
{articles_html}
</ul>

<div class="related">{related_html}</div>

<section class="transcript" id="transcript">
<h2>Full transcript</h2>
<p class="note">This is what is said in the video, with the figures written as numbers. Timestamps open the video at that point. The narration uses a digital clone of Steve Hunt's voice. The words are his own.</p>
{transcript_html}
</section>

{author_box()}
{DISCLAIMER.format(asat=AS_AT)}
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
<a href="{v['slug']}/"><img src="images/{v['slug']}.jpg" alt="{esc(v['title'])}" width="1280" height="720" loading="lazy"></a>
<div class="body">
<h2><a href="{v['slug']}/">{esc(v['title'])}</a></h2>
<p>{esc(v['short_answer'][0])}</p>
<p><a href="{v['slug']}/">Video, key facts and full transcript</a> &middot; {v['duration_text']}</p>
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
<p>Short videos that answer the questions families actually ask about UK inheritance tax: what the rules say, what things cost, and how the pieces fit together. The big one right now is the April 2027 change that brings unused pension funds into inheritance tax for the first time.</p>
<p>Every video on this site comes with its key facts, the legislation it relies on, the questions it answers, and a full transcript, so you can read it as well as watch it.</p>

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


def not_found_page():
    return f"""<!doctype html>
<html lang="en-GB">
<head>
{HEAD_COMMON}<title>Page not found | {esc(SITE_NAME)}</title>
<meta name="robots" content="noindex">
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
    urls = [(SITE + "/", TODAY.isoformat())] + [(f"{SITE}/{v['slug']}/", TODAY.isoformat()) for v in VIDEOS]
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
        f"LinkedIn: {LINKEDIN}",
        f"YouTube: {YOUTUBE_CHANNEL}",
        "",
        "## Videos with key facts and full transcripts",
        "",
    ]
    for v in VIDEOS:
        lines.append(f"- [{v['title']}]({SITE}/{v['slug']}/): {v['short_answer'][0]}")
    lines += ["", "## Notes", "", "Education only. Not advice, not a personal recommendation, and not an invitation to do business. Correct as at " + AS_AT + "."]
    return "\n".join(lines) + "\n"


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    write("index.html", home_page())
    for v in VIDEOS:
        write(f"{v['slug']}/index.html", video_page(v))
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
