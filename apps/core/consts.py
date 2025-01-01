from old.modules.random_events.entity.random_events import RandomEvent, RandomEventType


STICKER_LIST = [
    'CAACAgIAAxkBAAEK-yJlfqbwfqEbnBtdY1hcJmHs2Pu3cwACxRIAAo9wkEiKvM_KEU_KeDME',
    'CAACAgIAAxkBAAEK-yRlfqezvrHT-TFHYuW9FssJ8l47uAACiw4AAk7tyEhizTZbt7f0BzME',
    'CAACAgIAAxkBAAEK-yZlfqfth-fbyg8K58Pomfi6ZxvViwAC0AEAAoSjpCA7yWJajysO3TME',
    'CAACAgIAAxkBAAEK-yhlfqgM9crbNaO-75zsb83FBcrWdAACzgEAAoSjpCCdcKmRZ3kR6zME',
    'CAACAgIAAxkBAAEK-yplfqg31tYuIF37HkmSmmVt_0t9KQACCgAD8IE4B8Y05P0tF-2uMwQ',
    'CAACAgEAAxkBAAEK-yxlfqhdzrbS1Quq7L0MCz9fNGSJTgACuwADJJtYBpffPXFN4fjxMwQ',
    'CAACAgIAAxkBAAEK-y5lfqh87ioAAUWoH_m54kqEqZCDtKsAAhgBAAJhON8J7JpKtU1sj6AzBA',
    'CAACAgIAAxkBAAEK-zBlfqiWElEm96Ub6WjIDYw2XIWV1gACRBgAAt_v6UnnVUwXPPz3DzME',
    'CAACAgIAAxkBAAEK-zJlfqircMGq8UgEGks0XZyYXeUBSgACCgAD5MUZINg2vo7hFc86MwQ',
    'CAACAgIAAxkBAAELB4tliAWPxNfeeJTbr764GoC1XDwAAW4AAmAOAAJsoplI9oZRHFEQ5qgzBA',
    'CAACAgIAAxkBAAELB41liAWcoNwWwbdykXi9XuNCwAKsVgAC2A0AAm4iMUssGWH9Yv18-TME',
    'CAACAgIAAxkBAAELB49liAW6Ce3msuJLRn-HjhFJ3dIbhQACEicAArOsqUkP8s1xh5V08zME',
    'CAACAgIAAxkBAAELB5FliAXCuMJRExd2DrDuBf9UVjLcVQACrSEAAsrFqEn4TM0blTH5ijME',
    'CAACAgIAAxkBAAELB5NliAXNlEHc4DfFlrUV8C-csez2SwAClSUAAgZlsEkKDxkFFCsiTzME',
    'CAACAgIAAxkBAAELB5VliAX78_Hf4HzvoxJgpFwfqdTfiQACzAEAAoSjpCBda9dF1hrZNjME',
    'CAACAgIAAxkBAAELB5dliAYpRl0gdo1aNGVsRBnLOdmEpwACIQEAAmE43wmzKWzcfgLJHDME',
    'CAACAgIAAxkBAAELB5lliAYyJ6vyPdieCUSJZenveHfjigACoRoAAjNr8UlRn7snL37A0jME',
    'CAACAgIAAxkBAAELB5tliAY-2QrJsZ2pNQnnC7hec1oHCQACnS0AArg1SUk4l-5erVNphzME',
    'CAACAgIAAxkBAAELB51liAZFGizsPdNVBDj4CSbBOlHGJgACFgAD5MUZIE_F-je2lnbBMwQ',
    'CAACAgIAAxkBAAELB59liAZPl_kSP7kb8wcgrSSdvJFgNQAClxoAAoYjoUoq4AJsK_S8_jME',
    'CAACAgIAAxkBAAELB6FliAZWUgGgkPtDMwW_pSonVxtJIQAC9xcAAnDGoEoAAUyA7uGm0e4zBA',
    'CAACAgIAAxkBAAELB6NliAZkV_EJwksbLjfwxooxwVAAAbQAAnwAA57vdBAUHXMV6bZeeTME',
    'CAACAgIAAxkBAAELB6VliAZrPVSByhPTl_U0qnAAAa1fcxMAAn4AA57vdBBUNQNZojuo6TME',
    'CAACAgIAAxkBAAELB6dliAZ0xw5ImYKyA04vCt-MxmXavAACawADnu90EDFahe64cPdmMwQ',
    'CAACAgIAAxkBAAELB6lliAaA3AFWVtFtwE4K1pP-AazZigACrQADnu90EAn68BxCVwoSMwQ',
    'CAACAgIAAxkBAAELB6tliAarHjIRAXs_9PJEq1XqKqDsjQAC5gADmZhGEWxnT5BPbsVVMwQ',
    'CAACAgIAAxkBAAELB61liAa0fWFiCjaHCgEdqgqllfT4UAACDAEAApmYRhFMojNeNr7zQTME',
    'CAACAgIAAxkBAAELB69liAbgYa3HH_2LhOXwiIM1cv6LSgAC2x8AAp__QEgrNgjn50SsZzME',
    'CAACAgIAAxkBAAELB7FliAbpGdok2yduTuN1cJAGXPeAAAMfAQACYTjfCVlQaadGNbvKMwQ',
]

RANDOM_EVENTS = [
    RandomEvent(
        type=RandomEventType.MESSAGE,
        message='Что вершит судьбу человечества в этом мире? '
        'Некое незримое существо или закон, подобно '
        'Длани Господней парящей над миром? По крайне мере '
        'истинно то, что человек не властен даже над своей волей.',
    ),
    RandomEvent(
        type=RandomEventType.REPLY,
    ),
    *[
        RandomEvent(
            type=RandomEventType.STICKER,
            sticker=sticker_id,
        )
        for sticker_id in STICKER_LIST
    ],
]
