# Guide pages: one deep question-and-answer page per subject, drawn from Steve's
# LinkedIn articles and videos. Imported by build.py.

GUIDES = [
    {
        "slug": "nominees-annuity/guide",
        "parent": "nominees-annuity",
        "title": "The nominees' annuity: every question answered",
        "short_title": "Nominees' annuity guide",
        "seo_title": "Nominees' annuity: UK rules and inheritance tax from 2027",
        "seo_description": "The nominees' annuity explained: who can have one, the inheritance tax exclusion from April 2027, income tax, real quotations, and whether buying one is a gift.",
        "meta_description": (
            "The nominees' annuity, explained by Steve Hunt ACII TEP: what it is, who can be a nominee, how the "
            "inheritance tax exclusion from 6 April 2027 works, how the income is taxed, real quotations, and "
            "the unsettled question of whether buying one is a lifetime gift. Every answer links to the law."
        ),
        "published": "2026-10-02",
        "modified": "2026-10-03",
        "reviewed": "2026-10-02",
        "intro": (
            "This guide answers the questions people ask about the nominees' annuity. In everyday terms, that is "
            "whether a pension annuity can keep paying a son, daughter or grandchild after the parent dies, and what "
            "that means for inheritance tax from April 2027. It draws on Steve's LinkedIn articles, his video, the "
            "Acts and HMRC's published guidance. Each answer stands on its own and ends with its sources. Where an "
            "answer is Steve's own reading of the law rather than settled law, it says so."
        ),
        "short_answer": [
            "A nominees' annuity is an annuity paid to someone a pension member nominates, such as an adult child or "
            "grandchild, who is not a dependant under the pension tax rules. Bought in the member's lifetime together "
            "with the member's own lifetime annuity, the income carries on to the nominee for the rest of their life "
            "when the member dies, and from 6 April 2027 it is excluded from the member's estate for inheritance tax.",
            "The nominee's income is taxable if the member dies at 75 or over, and free of income tax if the member "
            "dies under 75. In August 2026 two insurers were quoting, both for nominees aged 40 or over. Whether buying "
            "one counts as a lifetime gift for inheritance tax has not been settled.",
        ],
        "short_sources": ["fa2004p27AA", "fa2004p27A", "ihta150A", "itepa646B", "tn333", "ptm072200", "q_age40"],
        "qa": [
            ("What is a nominees' annuity?",
             "An annuity payable to a nominee of a pension member. The law gives it two routes: bought together with "
             "a lifetime annuity payable to the member, where the member becomes entitled to that annuity on or after "
             "6 April 2015; or bought after the member's death, where the member died on or after 3 December 2014. "
             "This guide is about the first route, because that is the one excluded from inheritance tax. In everyday "
             "terms it is a joint life annuity where the second life is a child, grandchild or anyone else the member "
             "chooses, rather than a spouse or civil partner.",
             ["fa2004p27AA", "ptm072200"]),
            ("Who can be a nominee?",
             "An individual who has been nominated, by the member or by the scheme administrator, and who is not a "
             "dependant under the pension tax rules. A member's child under 23 is a dependant. A child aged 23 or "
             "over can be a nominee even if the member supports them financially, unless they are dependent because "
             "of physical or mental impairment or an older scheme's rules keep them as a dependant. For people other "
             "than the member's children, financial dependence on the member, mutual financial dependence, or "
             "dependence because of impairment can make them a dependant rather than a nominee. A spouse or civil "
             "partner is a dependant, not a nominee. A nominee need not be related to the member. A scheme "
             "administrator's nomination only counts while there is no dependant and no individual or charity "
             "nominated by the member for the relevant benefits.",
             ["fa2004p27A", "fa2004p15", "ptm071200", "tn333"]),
            ("What is the difference between one bought in the member's lifetime and one bought after death?",
             "Only the lifetime version is excluded from inheritance tax. A nominees' annuity bought in the member's "
             "lifetime, together with the member's own lifetime annuity, is an excluded benefit under section "
             "150A(6)(c) of the Inheritance Tax Act 1984 for a death on or after 6 April 2027. A nominees' annuity "
             "bought after the member's death, with unused funds, is a different route and is not in that list. Age "
             "at death matters to the income tax position of both, but the conditions differ: for an after-death "
             "purchase using unused uncrystallised funds, tax-free treatment also requires the nominee to become "
             "entitled within two years of the day the scheme administrator first knew, or could reasonably have "
             "been expected to know, of the death.",
             ["fa2004p27AA", "ihta150A", "itepa646B", "ptm072210", "tn333"]),
            ("Does it have to be one joint life contract?",
             "No. The law says the nominees' annuity must be purchased together with the member's lifetime annuity, "
             "and that means related to it. HMRC's manual explains that as the same contract, written on a joint "
             "life basis, or a separate contract with the same insurer or another one, bought within 7 days before "
             "or after the member's own annuity. A separate contract bought outside that window is not the "
             "lifetime-purchased related annuity discussed here.",
             ["fa2004p27AA", "ptm072200"]),
            ("Is a nominees' annuity excluded from inheritance tax from 6 April 2027?",
             "Yes, if it was purchased together with a lifetime annuity payable to the member. Section 150A of the "
             "Inheritance Tax Act 1984, inserted by the Finance Act 2026 for deaths on or after 6 April 2027, brings "
             "most unused pension money into the estate. Subsection (6)(c) lists a dependants' annuity or a nominees' "
             "annuity purchased together with a lifetime annuity payable to the member as an excluded benefit, and "
             "HMRC's technical note confirms there is no requirement for the other party to be a dependant of the "
             "member.",
             ["ihta150A", "fa2026s66", "fa2026s71", "tn333"]),
            ("Why is it bought with no guarantee period and no value protection?",
             "Because those extras count for inheritance tax, even though the nominee's annuity itself does not. The "
             "exclusion covers the annuity that carries on to the nominee. A guarantee period that keeps paying "
             "after death is brought into scope by HMRC's note as a continuing payment, and value protection that "
             "returns unused capital as a lump sum is not among the excluded benefits, so each would need its own "
             "assessment, after any exemptions and allowances. Having neither is not a condition of the exclusion; "
             "it is the choice made in the quotations in the video, so that nothing was left in scope.",
             ["ihta150A", "tn322", "tn333"]),
            ("Is the nominee's income taxable?",
             "It depends on the member's age at death. If the member dies at 75 or over, the income is taxed as pension "
             "income in the nominee's hands. If the member dies under 75, and the annuity was bought together with the "
             "member's own annuity with no payment before 6 April 2015, the income is free of income tax. In the video "
             "example Mr Miggins is already 75, so Amy's income is taxable.",
             ["itepa646B", "ptm072210", "inherit"]),
            ("Can the nominee get the income tax back through salary sacrifice?",
             "Possibly some of it. An employed nominee can give up salary in exchange for employer pension "
             "contributions, which lowers the income that is taxed, so in effect the parent's pension income "
             "replaces the salary and the salary goes into the nominee's own pension. The annuity itself stays "
             "taxable, and any saving depends on the nominee's earnings, their pension allowances and their "
             "employer. From 6 April 2029, salary-sacrificed pension contributions above £2,000 a year are scheduled "
             "to attract National Insurance; income tax relief on pension contributions is unchanged by that "
             "measure.",
             ["nics2026", "salsac", "itrates", "steve_p2"]),
            ("What does a nominees' annuity pay? The real quotations",
             "On 11 August 2026 Just quoted £29,153.64 a year, £2,429.47 a month, a rate of 5.83%, on a £500,000 "
             "fund for a father of 75 and a daughter of 45: level, no guarantee, no value protection, paid monthly "
             "in arrears, with 100% continuing to the daughter for life. On 10 August 2026 Canada Life quoted "
             "£28,925.76 a year, 5.79%, on the same terms. Both were at standard rates with no adviser charge. These "
             "are dated illustrations held on file, not recommendations, and rates may have changed since.",
             ["q_nominees", "steve_p2"]),
            ("What happens when the member dies?",
             "If the nominee outlives the member, the agreed income continues to the nominee for the rest of the "
             "nominee's life. In the quoted example the continuation is 100% of the gross income. The "
             "lifetime-purchased related annuity is kept out of the member's notional pension property by the "
             "statutory exclusion in section 150A(6)(c), not simply because the insurer pays the nominee directly. "
             "Executors may still need to consider whether the purchase involved a lifetime transfer that has to be "
             "reported.",
             ["fa2004p27AA", "ihta150A", "tn333"]),
            ("What happens if the nominee dies first, or both die early?",
             "The annuity ends when the last surviving named life dies. If the nominee dies before the member, the "
             "member's income continues for his lifetime and then stops. If both die early, with no guarantee period "
             "and no value protection, nothing more is paid. That is a risk of the contract illustrated here, not a "
             "condition of the tax exclusion. One way to protect against it is life assurance on the nominee's own "
             "life, in trust: term cover protects only for its term, premiums must be kept up, and total premiums "
             "can exceed the payout. Whether that is worth doing depends on the family's circumstances.",
             ["q_nominees", "steve_p2"]),
            ("Can a widow buy a nominees' annuity with the pension she inherited?",
             "No. The excluded version must be purchased together with a lifetime annuity payable to the member, and "
             "she was not the member; her husband was. The opportunity to arrange it ended when he died. She can still "
             "buy an annuity on her own life with what she inherited, and she can buy a nominees' annuity with her own "
             "pension, because she is the member of that.",
             ["fa2004p27AA", "ihta150A", "steve_p2"]),
            ("Can a member set up nominees' annuities for more than one child?",
             "Yes. Nothing in the pension rules limits a member to one nominee. A member with two children can buy two "
             "nominees' annuities, one for each child, each with its own slice of the fund, bought in his lifetime "
             "alongside his own annuity. The insurers take one second life per contract, and in August 2026 wanted each "
             "nominee to be 40 or over, so each one is quoted separately. Each purchase raises the same unsettled gift "
             "question answered below.",
             ["fa2004p27AA", "ptm072200", "q_age40"]),
            ("Why do insurers want the nominee to be 40 or over?",
             "That is the insurers' own condition, not the law. In August 2026 the two insurers who quoted both drew "
             "their line at age 40. In law the nominee can be any age, although a member's own child under 23 is a "
             "dependant, not a nominee. The other insurers asked at the time said no, though some were reviewing. "
             "Steve's expectation in August 2026 was that the age condition would not move before April 2027; that "
             "is his forecast, and the market may have changed since.",
             ["fa2004p27A", "fa2004p15", "q_age40", "steve_p2"]),
            ("Can a nominees' annuity bring an estate back under the £2 million taper?",
             "On the arithmetic, yes, leaving aside the unsettled gift question below. Steve's example from July "
             "2026: a widower of 69 with a £1 million pension and a £2.5 million estate including it, everything to "
             "his son, aged 39. Die on 7 April 2027 and the pension counts, the estate is £500,000 over the £2 "
             "million taper threshold, the residence nil rate bands fall from £350,000 to £100,000, and the bill is "
             "£700,000. Use the whole £1 million to buy his own lifetime annuity with a nominees' annuity for his "
             "son, purchased together, and the estate falls to £1.5 million, the residence bands are fully restored, "
             "and the bill on the same death is £200,000. The son would get an income for life, tax free if his "
             "father died before 75. The example assumes the full transferred bands are available and claimed, that "
             "a home of enough value passes to the son, and that nothing else, such as other gifts, reliefs or death "
             "benefits, disturbs the sums; the annuity rate was an estimate. It is an illustration, not an available "
             "quotation: the son was 39, and the insurers quoting in August 2026 wanted the nominee to be 40 or "
             "over.",
             ["ihta150A", "ihta8D", "rnrb", "itepa646B", "steve_p1"]),
            ("Is buying a nominees' annuity a lifetime gift for inheritance tax?",
             "Nobody has settled it, and this guide does not settle it. What follows is Steve's analysis, not HMRC's "
             "published position. His reading: buying the continuation for another person out of a pension may be a "
             "transfer of value, because it can leave the member's estate smaller, and if the conditions for a "
             "potentially exempt transfer are met it may be a PET. The exclusion at death in section 150A does not "
             "answer that lifetime question. On his reading, before 6 April 2027 the answer may be yes, and after 6 "
             "April 2027 it turns on whether what the member holds over the pension is a right or a general power, "
             "explained in the next question. HMRC's technical note says the 2027 changes do not alter the existing "
             "position for lifetime transfers, but that passage is about money taken out of a pension and then given "
             "away; it does not expressly decide this purchase. HMRC's manual says lifetime charges from changes to "
             "pension rights generally arise only where the member was in ill health. Pension lifetime transfers "
             "have reached the Supreme Court, in HMRC v Parry in 2020, but that case concerned a different "
             "transaction and does not decide this one. The full argument is in Osborne's Get Out of Jail Card Under "
             "Attack.",
             ["ihta3", "ihta3A", "ihta150A", "tn1125", "ihtm17041", "parry", "steve_pet"]),
            ("Why does it matter whether a pension is a right or a power?",
             "Because the Act counts them differently, and this is the heart of Steve's analysis. Your estate is the "
             "property you are beneficially entitled to (section 5(1)). Section 5(2) adds property you do not own "
             "but have a general power to dispose of as you think fit, except settled property, meaning property in "
             "a trust; a general power is a specific test, and not every power, request or nomination over a pension "
             "meets it. Section 151(4) says that for pension schemes the words 'other than settled property' are "
             "treated as omitted, so until 6 April 2027 a pension trust over which the member holds a general power "
             "counts as his, and giving part of it away can be a gift. From 6 April 2027 the Finance Act 2026 omits "
             "section 151(4) and replaces section 151(3) with a rule that sections 49 to 53 do not apply to pension "
             "property. After that, on Steve's reading, a settlement power over the fund no longer counts, because "
             "section 272 says property does not include a settlement power; but a right to benefits is property, "
             "counts under section 5(1), and would count before and after April 2027. Rights and powers can exist "
             "side by side, and which a member holds depends on the scheme and the contract. Other pension and "
             "family legislation generally describes a member's lifetime position as rights, which is why Steve "
             "thinks a right is the more likely answer, though words elsewhere do not settle the tax question. Even "
             "if the pension counts, a gift still needs a loss to the estate and the PET conditions to be met. This "
             "is his reading of the words, not a ruling, and no court has decided this particular question.",
             ["ihta5", "ihta151", "ihta151old", "fa2026s69", "ihta272", "ihta3A", "steve_pet"]),
            ("If it is a gift, how big would it be?",
             "The statutory starting point is the loss to the member's estate on the day. This guide does not "
             "establish an accepted valuation for this purchase, and what follows is Steve's illustrative "
             "income-ratio calculation, not an actuarial valuation or an HMRC-approved method. In round numbers: a "
             "pot that would buy a single life annuity of £10,000 a year buys £5,000 a year instead so that 100% "
             "continues to his son, so he has given up half the income, and half of a £100,000 pot is £50,000. On "
             "real quotations run on 19 September 2026, a pot of £99,368.63 bought £10,000 a year single life or "
             "£6,084.36 a year with a 45-year-old second life, a drop of 39.16% (39.1564% unrounded), which applied "
             "to the pot gives £38,909.18, and £15,563.67 of tax at 40% if death came within three years with no "
             "allowances left. HMRC's actuaries would value a real case on age and health, and the figure could be "
             "larger or smaller.",
             ["ihta3", "gifts", "q_sept", "steve_pet"]),
            ("If it is a gift, when does the seven-year clock start, and what happens on death within seven years?",
             "If the purchase is a potentially exempt transfer, the clock starts on the day the annuity is bought. A "
             "PET made seven years or more before death is exempt; any other becomes chargeable. A chargeable gift "
             "uses up the nil rate band before the estate does, so a gift within the band reduces what is left for "
             "the estate, and a gift above it may itself bear tax. Where the gift itself is taxed, taper relief "
             "reduces the tax if the gift was made more than three years before death: 80% of the full rate at three "
             "to four years, down to 20% at six to seven years. Taper reduces the tax, not the size of the gift.",
             ["ihta3A", "ihta7", "gifts"]),
            ("Where would it be reported after death?",
             "On both pension and gift forms, which work together. Form IHT409, pensions, asks whether the deceased "
             "transferred, nominated, assigned or changed pension benefits in the two years before death. HMRC's "
             "notes to the main form say that if you want to include your own value for pension benefits given away, "
             "you enter it on form IHT403, gifts and other transfers of value, and explain how you arrived at it. So "
             "if the purchase were a gift, its value would sit on IHT403 with the explanation on IHT409. That is one "
             "reason the point is easy to miss.",
             ["iht400notes", "iht403", "iht409", "steve_pet"]),
            ("Is there a two-year rule?",
             "Not a rule that settles it, and not a safe harbour. HMRC's manual says that where a transfer of "
             "pension rights was made more than two years before death, HMRC can generally assume the member was in "
             "normal health unless there is evidence otherwise, and that lifetime charges from changes to pension "
             "rights generally involve a loss to the estate only where the member was in ill health at the time. "
             "Form IHT409 asks about changes to pension benefits in the two years before death. That is HMRC's "
             "enquiry practice, not a statutory exemption after two years, and it is a different two-year period "
             "from the one that affects the income tax position of an annuity bought after death. Buying a nominees' "
             "annuity in good health, well before death, is a different thing from a change made on a deathbed.",
             ["ihtm17070", "ihtm17041", "iht409", "steve_p1"]),
            ("How can the seven-year risk be covered?",
             "For the possible failed-gift liability discussed here, the relevant cover is on the member's life. A "
             "policy held in a suitable trust can provide money to the trustees outside the member's estate following "
             "a covered death, subject to the conditions below. Cover for a fixed term and whole of life "
             "cover last for different periods: term cover ends when the term ends, while whole of life pays "
             "whenever death occurs, including after the seven years when a PET would no longer fail. So whole of "
             "life would pay in the seven-year window and beyond it; its payout is not confined to a failed gift. "
             "The tax position has its own conditions. An annuity and a life policy on the same life can be treated "
             "as associated operations under sections 263 and 268 of the Inheritance Tax Act 1984; HMRC's Statement "
             "of Practice E4 treats them as not associated where the policy was issued on full medical evidence, at "
             "minimum a private medical attendant's report used in normal underwriting, and would have been issued "
             "on the same terms if the annuity had not been bought. Premiums are only exempt as normal expenditure "
             "out of income if all three conditions in section 21 are met: part of the person's normal expenditure, "
             "made out of income taking one year with another, and leaving enough income to keep their usual "
             "standard of living; and section 21 has a special rule where an annuity has been bought on the same "
             "life. Whether cover suits a family, the amount, the exclusions and keeping up the premiums all need "
             "separate consideration. Whole of life assurance has its own page on this site.",
             ["ihta263", "ihta268", "ihta21", "ihtm20211", "ihtm20375", "steve_pet"]),
            ("Does a nominees' annuity lose value with inflation, and can it be undone?",
             "A level annuity pays the same amount for life, so its buying power falls with inflation; escalating "
             "versions start lower. Once the cancellation period has passed, an annuity purchase normally cannot be "
             "reversed, so the decision is for the member's life and the nominee's life after that. The quotations "
             "above were all level.",
             ["q_nominees", "steve_history"]),
            ("How does it compare with leaving the pension fund to the child?",
             "From 6 April 2027 an unused fund left at death counts in the estate. After the exemptions and "
             "allowances available, the exposure is 40%, with a marginal effect of 60% on the slice that tapers away "
             "the residence nil rate band, plus income tax on withdrawals if death is at 75 or over. The site's "
             "worked example on the pensions page, with all its assumptions, shows a £500,000 fund costing a family "
             "£516,000 in extra inheritance tax and income tax combined, across the family, not deducted from the "
             "pension itself. A nominees' annuity bought in the member's lifetime with his own annuity is excluded, "
             "so that inheritance tax does not arise on it, and the nominee pays income tax on the income only if "
             "the member died at 75 or over. The price is that the capital becomes an income for two lives, with no "
             "lump sum, and in the example no guarantee, no value protection and no inflation protection. The "
             "unsettled gift question sits on top.",
             ["ihta150A", "ihta8D", "rnrb", "itepa646B", "pensions_example"]),
            ("Where did the nominees' annuity come from?",
             "From George Osborne. In March 2014 he said no one would have to buy an annuity, and annuity sales fell "
             "sharply over the next two years. On 29 September 2014 he announced that anyone dying under 75 could "
             "pass an unused pension fund to anybody tax free, but not an annuity. On 3 December 2014 the government "
             "levelled that up: annuity income could pass to anyone too, on the same tax-free basis. The Taxation of "
             "Pensions Act 2014 added the definition of a nominee to the pension tax rules, and the Finance Act "
             "2015, which received Royal Assent on 26 March 2015, added paragraph 27AA, the nominees' annuity, from "
             "6 April 2015. In Steve's experience nothing then happened for more than a decade: he found no "
             "mainstream insurer marketing one, and the first quotations he obtained were in August 2026, from Just "
             "and Canada Life. When Parliament wrote the 2027 rules it named the nominees' annuity and excluded it.",
             ["tpa2014", "fa2015", "fa2004p27AA", "ihta150A", "steve_p1", "steve_history"]),
        ],
        "articles": [
            ("jail", "Part Four: is buying one a gift? The right or power argument in full, with the hedge."),
            ("oneword", "Part Two: the Mr Miggins and Amy figures, the insurers' answers, and the age 40 condition."),
            ("killed", "Part One: where the nominees' annuity came from, and the £2 million taper example."),
            ("husband", "Part Three: what happens to a pension left to a widow, the £516,000 example."),
        ],
        "keywords": ["nominees' annuity", "nominee annuity", "joint life annuity", "pension inheritance tax 2027",
                     "potentially exempt transfer", "Finance Act 2004 Schedule 28 paragraph 27AA",
                     "Inheritance Tax Act 1984 section 150A", "section 151(4)"],
    },
    {
        "slug": "pensions-and-inheritance-tax-from-april-2027/guide",
        "parent": "pensions-and-inheritance-tax-from-april-2027",
        "title": "Pensions and inheritance tax from April 2027: every question answered",
        "short_title": "Pensions and IHT 2027 guide",
        "seo_title": "Pensions and inheritance tax from April 2027: every question answered",
        "seo_description": "From 6 April 2027 unused pensions count for inheritance tax. What is caught, what is excluded, who pays, income tax on top, and the £516,000 example.",
        "meta_description": (
            "Pensions and inheritance tax from 6 April 2027, explained by Steve Hunt ACII TEP: what is caught, what "
            "is excluded, who pays and when, the Pensions Direct Payment Scheme, income tax on top, and the £516,000 "
            "worked example. Every answer links to the law."
        ),
        "published": "2026-10-03",
        "modified": "2026-10-03",
        "reviewed": "2026-10-03",
        "intro": (
            "This guide answers the questions people ask about pensions and inheritance tax from 6 April 2027, such "
            "as whether a family will pay inheritance tax on a parent's unspent pension, and who pays it. It draws "
            "on Steve's LinkedIn articles, his video, the Finance Act 2026 and HMRC's two technical notes of May and "
            "August 2026. Each answer stands on its own and ends with its sources. Where an answer is Steve's own "
            "reading rather than settled law, it says so. HMRC expects to publish a third technical note in the "
            "autumn and its detailed guidance by April 2027, and this guide will be reviewed against them."
        ),
        "short_answer": [
            "From 6 April 2027, most unused pension funds and pension death benefits count as part of the estate for "
            "inheritance tax, under section 150A of the Inheritance Tax Act 1984. Pensions left to a spouse, civil "
            "partner or charity are usually exempt, subject to the conditions of those exemptions, and four kinds of "
            "benefit are excluded altogether, including qualifying death in service benefits and joint life "
            "annuities bought together with the member's own annuity.",
            "The personal representatives report the pension and are liable for the tax, which is due by the end of "
            "the sixth month after the month of death and which the scheme can pay straight to HMRC on a valid "
            "request. If the member died at 75 or over, the beneficiary also pays income tax on what they draw, but "
            "not on the part that pays the inheritance tax on the pension. Where a pension takes an estate over £2 "
            "million the combined cost can be severe: in the site's worked example, on its stated assumptions, a "
            "£500,000 pension costs a family £516,000.",
        ],
        "short_sources": ["ihta150A", "fa2026s71", "ihta18", "ihta23", "tn22", "ihta226", "ihta226B", "itepa567B", "pensions_example"],
        "qa": [
            ("What changes for pensions and inheritance tax on 6 April 2027?",
             "For deaths on or after 6 April 2027, most unused pension funds and pension death benefits count as part "
             "of the estate for inheritance tax. Section 150A of the Inheritance Tax Act 1984, inserted by the "
             "Finance Act 2026, treats a member of a registered pension scheme (or of a qualifying non-UK or section "
             "615(3) scheme) as beneficially entitled, immediately before death, to what it calls notional pension "
             "property. Above the nil rate bands that can mean tax at 40%. Pensions left to a spouse or civil partner "
             "are usually exempt, subject to the conditions of the spouse exemption, and some benefits are excluded "
             "altogether.",
             ["ihta150A", "fa2026s66", "fa2026s71", "tn12", "ihta18"]),
            ("Why were most pensions outside inheritance tax before April 2027?",
             "Because most pension schemes pay death benefits at the discretion of the scheme's trustees or provider. "
             "Until they decide, nobody is entitled to the money, so in most cases it was not part of anyone's "
             "estate. It already counted where it was payable to the estate as of right, or where the member could "
             "make a binding nomination or otherwise had a general power over it. From 6 April 2027 trustee "
             "discretion no longer decides whether a pension is in scope, although it still matters for who receives "
             "it and when.",
             ["ihtm17051", "ihtm17052", "tn21"]),
            ("What is notional pension property?",
             "It is the Act's name for the pension value that section 150A treats the member as owning, immediately "
             "before death, for inheritance tax. For a money purchase pension it is broadly the fund that may or must "
             "be used to provide benefits on death; for a defined benefit scheme it is the lump sum death benefits "
             "and guaranteed continuing payments; excluded benefits are taken off. In Steve's analysis the word "
             "notional carries the whole change: the member is treated as owning the pension for the charge, yet "
             "HMRC's technical note says the member is not treated as owning the pension's assets when it rules out "
             "business property relief, agricultural property relief, loss on sale relief and payment by instalments.",
             ["ihta150A", "tn321", "tn322", "tn1121", "tn1123", "tn1124", "steve_p2"]),
            ("Does it apply if someone dies before 6 April 2027?",
             "No. The change applies to deaths on or after 6 April 2027. If the member dies before that date, the "
             "current rules apply, even if the benefits are paid to the beneficiaries after it.",
             ["fa2026s71", "tn12"]),
            ("Which pensions are caught?",
             "Unused money in personal pensions, SIPPs and money purchase workplace schemes, including drawdown "
             "funds, and lump sum death benefits and guaranteed continuing payments from defined benefit schemes. "
             "Qualifying non-UK pension schemes and section 615(3) schemes are caught too. For money purchase "
             "pensions the count also includes amounts not held in the member's own pot where they can reasonably be "
             "expected to be used to pay death benefits, such as cash balance benefits or an expected augmentation.",
             ["ihta150A", "tn321", "tn322", "tn26"]),
            ("Which pension benefits are excluded?",
             "Four kinds, listed in section 150A(6): a dependants' scheme pension, from any type of arrangement; a "
             "trivial commutation lump sum that replaces a dependants' scheme pension; a dependants' or nominees' "
             "annuity bought together with the member's own lifetime annuity; and death in service benefits, meaning "
             "benefits payable only because the member was in employment or other work immediately before death. The "
             "test is what the scheme allows, not only what is chosen after the death: a benefit is excluded only "
             "where it may only be paid in one of those forms. HMRC's August 2026 note says that if a dependant could "
             "have used the fund to buy a dependants' annuity but chooses a dependants' scheme pension, that pension "
             "is not excluded. Other benefits payable on death are counted, valued as section 150A sets out.",
             ["ihta150A", "tn331", "tn332", "tn333", "tn334", "tn2_dsp"]),
            ("Are annuity guarantee periods and value protection included?",
             "Yes. Where payments carry on to someone else after death under a guarantee period, they are brought "
             "into scope, and value protection, which returns unused capital as a lump sum death benefit, is not an "
             "excluded benefit either. A single life annuity with neither has no death benefit, so there is nothing "
             "left in it to count when the annuitant dies. HMRC's August 2026 note gives the example of an annuity "
             "that ceased on death, valued at nil.",
             ["ihta150A", "tn322", "tn2_ex1"]),
            ("Are death in service benefits included?",
             "Not if they qualify for the exclusion. It covers benefits payable because the member was employed, or "
             "in other work of a particular description, immediately before death, and that would not be payable "
             "otherwise. A refund of contributions that would have been paid anyway is not covered. Lump sums from "
             "the scheme of a previous job, where the member was a deferred member, normally are not covered either, "
             "although someone who left under a redundancy package may still count as employed under its terms or the "
             "scheme rules. Employers and schemes decide whether people on career breaks or long-term sickness "
             "absence count as in employment.",
             ["ihta150A", "tn334", "tn2_deferment"]),
            ("Is a pension left to a husband, wife or civil partner taxed?",
             "Usually there is no inheritance tax, subject to the spouse-exemption conditions. Benefits that go to a "
             "spouse or civil partner are exempt under section 18. The main exception: where the person who died was "
             "a long-term UK resident and their spouse or civil partner is not, the exemption is capped at the nil "
             "rate band limit, less any amount already used. Unmarried partners are not covered. The exemption defers "
             "the tax rather than removing it: if the survivor still holds the money when they die on or after 6 "
             "April 2027, it can count in their estate then, and unless they have remarried there is no spouse "
             "exemption to use. It is an inheritance tax exemption only, and does not make the pension income free of "
             "income tax.",
             ["ihta18", "tn34", "steve_p2"]),
            ("Does an inherited pension count in the estate of the person who inherited it?",
             "Yes, remaining inherited drawdown can count on the beneficiary's death on or after 6 April 2027. HMRC's "
             "August 2026 technical note expressly illustrates money inherited before April 2027 being included when "
             "the beneficiary later dies. In its example a mother dies in July 2026, her son puts his share into "
             "beneficiary drawdown, and when he dies in November 2030 what is left in that account counts as his "
             "notional pension property, alongside his own pensions. The site's worked example rests on the same "
             "point: Mrs Miggins inherits her husband's pension before April 2027 and dies in 2029 with it still in "
             "drawdown. Money already paid out of the scheme to the beneficiary is part of their ordinary estate "
             "instead.",
             ["ihta150A", "tn2_beneficiary", "pensions_example"]),
            ("Who is responsible for paying the inheritance tax on a pension?",
             "The personal representatives. They report the pension and are liable for the tax on it. Once the "
             "pension is vested in a beneficiary, meaning the trustees have decided who receives it (or, in a "
             "non-discretionary scheme, the beneficiary is identified under the scheme rules), that beneficiary "
             "becomes jointly and severally liable with them for the tax attributable to it. The pension scheme "
             "administrator is not normally liable, unless it fails to act on a valid withholding notice or payment "
             "notice.",
             ["fa2026s67", "tn21", "tn22"]),
            ("When must the tax be paid?",
             "By the end of the sixth month after the month of death, as for the rest of the estate. Interest runs on "
             "anything unpaid after that. The ten-year instalment option is not available for pension funds.",
             ["ihta226", "ihta233", "tn23", "tn1124"]),
            ("Does the tax on the pension have to be paid before probate?",
             "Normally, yes. HMRC's note says personal representatives must pay the inheritance tax due at that "
             "stage, including on pensions, and submit an account before they can apply for probate. In some cases "
             "HMRC will agree to postpone payment of some of the tax, with interest still running. The pension's "
             "share can be paid by the scheme under a payment notice, which can be used before probate is granted.",
             ["tn10", "ihtm05120", "tn7"]),
            ("Can the pension scheme pay the tax straight to HMRC?",
             "Yes, on a valid request. Under the Pensions Direct Payment Scheme, the personal representatives, or a "
             "beneficiary (including the trustees of a trust that benefits), can give the scheme administrator a "
             "payment notice for the tax they are liable for on the pension. The scheme must pay HMRC within 35 days "
             "of receiving a valid notice. The notice must be for at least £1,000, cannot exceed the tax and interest "
             "the person giving it is liable for on the pension in that scheme, and cannot exceed the benefits still "
             "unpaid, after deducting anything already paid out or already covered by an earlier payment notice. It "
             "is optional, a prospective personal representative cannot give one, and money already "
             "used to secure an annuity counts as paid out, so it is not available.",
             ["ihta226B", "fa2026s68", "tn7", "tn732", "tn2_validity", "tn74"]),
            ("Can the personal representatives hold back the pension until the tax is paid?",
             "Partly. A personal representative, or a prospective one, meaning someone with reason to believe they "
             "will become a personal representative, who knows or has reason to believe they may be liable for "
             "inheritance tax on the pension can give a withholding notice. While it has effect, the scheme cannot "
             "pay a beneficiary more than half of their entitlement, counting anything already paid. It lasts until "
             "the tax and interest are paid, the notice is withdrawn, or 15 months after the end of the month of "
             "death, whichever comes first. It does not change when the tax is due, and it does not apply to excluded "
             "benefits or to exempt beneficiaries such as a spouse.",
             ["ihta226A", "fa2026s68", "tn6", "tn2_amount"]),
            ("Does the pension pay the inheritance tax it causes?",
             "Not necessarily. The tax on an estate is shared across the parts that bear it, in proportion to their "
             "values, so the pension bears its proportionate share of the whole bill. That share is a different "
             "calculation from the extra tax that adding the pension caused, and the two need not match. A payment "
             "notice is limited to the tax on the pension. In the site's worked example the pension's share is "
             "£140,000 of a £300,000 increase in the estate's tax, so £160,000 falls on the rest of the estate.",
             ["ihta265", "ihta226B", "tn732", "pensions_example"]),
            ("How do personal representatives find the pensions and their values?",
             "They should take reasonable steps to identify every scheme, then ask each one for the basic "
             "information. Regulations made on 13 July 2026 (SI 2026/818) set the timetable from 6 April 2027. The "
             "value of the pension, or an estimate with an explanation of how it was reached, is due within 28 "
             "days of a valid request, and an estimate must be followed by the actual value within 14 days of it "
             "being known. Information dependent on deciding the beneficiaries is due by the later of the "
             "applicable 28-day deadline and the end of the 14-day period beginning when all beneficiaries are "
             "decided. Further information is required where an inheritance tax account must be filed, even if no "
             "tax is due. If a pension turns up after the account has gone in, a corrective account is needed.",
             ["si2026818", "tn25", "tn2_basic", "tn2_pexempt", "tn2_further", "tn4"]),
            ("Will the people who inherit also pay income tax?",
             "It depends on the type of benefit and on whose death it follows. As a general rule, if the person died "
             "at 75 or over, death benefits paid to people are taxable as the recipient's income. If they died under "
             "75, survivors' annuities and beneficiary drawdown are usually tax free, and many lump sums are tax free "
             "within the deceased's lump sum and death benefit allowance, some only if paid within two years. There "
             "are exceptions: a trivial commutation lump sum death benefit is taxable whatever the age, and "
             "dependants' scheme pensions are always taxable as pension income, even where they are excluded from "
             "inheritance tax. "
             "Where a pension passes on a second time, the successor's position depends on the age at death of the "
             "previous beneficiary, not the original saver. That is why Amy's withdrawals in the site's example are "
             "taxable after her mother dies at 75 or over, even though her father died under 75.",
             ["tn8", "inherit", "ptm072430", "ptm073700", "ptm073400"]),
            ("Is income tax charged on the part of the pension used to pay inheritance tax?",
             "No. Where the statutory conditions are met, pension income can be reduced by the inheritance tax and "
             "interest attributable to those pension death benefits and borne by the beneficiary. This is not a "
             "deduction for the extra inheritance tax attributable to other estate assets. If the scheme pays the "
             "tax under a payment notice, the benefits are reduced first, so income tax falls only on what is "
             "left. If the beneficiary bears the tax another way, they can reduce their taxable pension income by "
             "working with HMRC.",
             ["itepa567B", "fa2026s70", "tn82"]),
            ("Why do people say an inherited pension can be taxed at 87% or more?",
             "The 87% is a simplified illustration of the combined family tax, not a tax rate in law, and it is not "
             "all taken from the pension. It adds three layers for each pound of pension that takes an estate over £2 "
             "million: 40% inheritance tax; a further 20% because the residence nil rate band is withdrawn at £1 for "
             "every £2, a cost that can fall on the rest of the estate; and, if death was at 75 or over, income tax "
             "at 45% for an additional rate taxpayer on the 60% assumed to be left in the pension. So 40% + 20% + "
             "(45% × 60%) = 87%. In a real estate the pension's own share of the tax is worked out under section 265 "
             "and can be smaller, which leaves more in the fund to be taxed as income, and a beneficiary in the "
             "£100,000 to £125,140 band pays an effective 60% on it (rates outside Scotland). In Steve's analysis "
             "that is how the site's worked example reaches £516,000 on a £500,000 pension.",
             ["ihta8D", "ita35", "itrates", "ihta265", "steve_p3"]),
            ("Can the tax on a £500,000 pension really come to £516,000?",
             "In a specific case built on stated assumptions, yes, and the site's worked example shows every step. "
             "Mrs Miggins inherits a £500,000 pension from her husband, who died under 75 before April 2027, and "
             "dies in 2029, aged 75 or over, with an estate of £2 million before the pension, both their nil rate "
             "bands available in full and a home passing to her daughter. The pension raises her estate's "
             "inheritance tax from £400,000 to £700,000, an extra £300,000, of which the pension's own share is "
             "£140,000. Her daughter Amy, earning £100,000, draws the remaining £360,000 at £24,000 a year for 15 "
             "years and pays £216,000 of income tax at an effective 60%. That is £516,000 across the family. The "
             "example assumes the full transferable ordinary and residence nil rate bands before tapering, "
             "sufficient qualifying residential inheritance, no other material gifts or reliefs, and no investment "
             "growth or other changes. It holds today's tax rules and Amy's earnings constant for 15 years, so it "
             "is an illustration, not a forecast or a typical result.",
             ["pensions_example", "ihta8D", "ihta265", "ita35", "steve_p3"]),
            ("Can business property relief, agricultural property relief or instalments apply to a pension?",
             "No. HMRC's technical note says the member is not treated as owning the pension's assets, and on that "
             "basis rules out business property relief, agricultural property relief, loss on sale relief and payment "
             "by instalments for pension funds. Quick succession relief does apply where the same money is taxed "
             "again within five years.",
             ["tn1121", "tn1122", "tn1123", "tn1124", "ihta141"]),
            ("Does leaving pension money to charity reduce the tax?",
             "Yes. Pension death benefits paid to a UK charity are exempt, as other gifts to charity are. "
             "Separately, if at least 10% of the baseline amount of the relevant part of the estate goes to "
             "charity, that part is taxed at 36% instead of 40%. Broadly, the baseline allows for the available "
             "ordinary nil rate band and relevant reliefs and exemptions, but adds back the charitable gift and "
             "does not deduct the residence nil rate band. Pension money counts in the general part of the estate "
             "for this test, with charity lump sum death benefits counting towards the 10%. A charity lump sum "
             "death benefit is free of income tax even if the member was 75 or over, but it is only available from "
             "money purchase funds where there are no dependants when it is paid, and it must go to a charity "
             "nominated by the member or, for an inherited fund, by the deceased beneficiary.",
             ["ihta23", "ihtasch1A", "ihtm45009", "tn34", "tn111", "ptm073900"]),
            ("Are overseas pensions caught?",
             "Yes, for long-term UK residents: notional pension property in registered schemes, qualifying non-UK "
             "pension schemes and section 615(3) schemes counts, wherever the scheme is established. For someone who "
             "is not a long-term UK resident, only schemes established in the UK count. Withholding notices and "
             "payment notices cannot be given to qualifying non-UK pension schemes or section 615(3) schemes.",
             ["ihta150A", "tn26", "tn351"]),
            ("Will the nil rate bands go up?",
             "Not under the current law before April 2031. The nil rate band of £325,000, the residence nil rate band "
             "of £175,000 and the £2 million taper threshold are frozen, with no indexation, up to and including the "
             "2030-31 tax year. The Finance Act 2026 extended the freeze by a year.",
             ["fa2021s86", "fa2026s72", "ihtgov", "rnrb"]),
            ("Can money drawn from a pension be given away free of inheritance tax?",
             "It can, if the gift is exempt or, for an outright gift to another person, the giver survives seven "
             "years. HMRC's note confirms the April 2027 changes do not alter the existing rules for lifetime gifts. "
             "The exemption for normal expenditure out of income has three conditions, tested on the facts, taking "
             "one year with another: part of the giver's normal expenditure, made out of income, and leaving enough "
             "income to keep their usual standard of living. How the withdrawal was taxed does not by itself decide "
             "that. Money drawn from your own pension is normally taxed as income beyond any tax-free cash, while "
             "withdrawals from an inherited pension can be tax free where the person who died was under 75. An "
             "outright gift to an individual that is not exempt is normally a potentially exempt transfer, free of "
             "inheritance tax if the giver survives seven years and keeps no benefit from it. A gift into most trusts "
             "is a chargeable lifetime transfer instead, and surviving seven years does not simply make it exempt.",
             ["tn1125", "ihta21", "ihta3A", "ihta7", "fa1986s102", "inherit"]),
            ("What can people do about it in their lifetime?",
             "This guide does not recommend anything, and what suits one family can cost another. The routes most "
             "discussed are: keeping the pension to meet retirement needs; spending or drawing it, which brings "
             "income tax forward; giving away money drawn from it, under the normal gift rules; leaving it to a "
             "spouse, civil partner or charity; buying an annuity, where a single life annuity with no guarantee or "
             "value protection leaves nothing to count, as HMRC's August 2026 note illustrates, and a dependants' or "
             "nominees' annuity bought with the member's own is excluded; and life cover written in trust to provide "
             "money for the tax. Each has its own conditions and costs, some cannot be undone, and whether any is "
             "worth doing depends on the person's circumstances.",
             ["ihta3A", "ihta21", "ihta18", "ihta23", "ihta150A", "tn333", "tn2_ex1", "steve_p2"]),
            ("How much pension money comes within inheritance tax?",
             "The scale of UK defined contribution pension assets is over £1 trillion. The Pensions Policy "
             "Institute's DC Future Book 2025 reports aggregate assets of £1.2 trillion in 2024. Steve uses that "
             "published figure to illustrate the scale of the pension category affected by section 150A; it is not "
             "an official estimate of the precise value newly taxable in April 2027 or of tax to be collected. "
             "Amounts may be spent, pass to exempt recipients or fall within available allowances, so being within "
             "the rules does not mean every pound is taxed.",
             ["ppi2025", "pa1trn", "ihta150A", "ihta18", "ihta23", "steve_p2"]),
        ],
        "articles": [
            ("husband", "The £516,000 worked example, Mrs Miggins and her daughter Amy."),
            ("oneword", "The word \"notional\", and why the reliefs do not apply."),
        ],
        "keywords": ["pensions inheritance tax April 2027", "inheritance tax on pensions", "notional pension property", "Inheritance Tax Act 1984 section 150A", "Finance Act 2026", "Pensions Direct Payment Scheme", "pension death benefits income tax", "residence nil rate band taper"],
    },
]
