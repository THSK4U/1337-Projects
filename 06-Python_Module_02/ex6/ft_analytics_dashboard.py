data_list = {
    'players': {
        'alice': {
            'level': 41,
            'total_score': 2824,
            'sessions_played': 13,
            'favorite_mode': 'ranked',
            'achievements_count': 5
        },
        'bob': {
            'level': 16,
            'total_score': 4657,
            'sessions_played': 27,
            'favorite_mode': 'ranked',
            'achievements_count': 2
        },
        'charlie': {
            'level': 44,
            'total_score': 9935,
            'sessions_played': 21,
            'favorite_mode': 'ranked',
            'achievements_count': 7
        },
        'diana': {
            'level': 3,
            'total_score': 1488,
            'sessions_played': 21,
            'favorite_mode': 'casual',
            'achievements_count': 4
        },
        'eve': {
            'level': 33,
            'total_score': 1434,
            'sessions_played': 81,
            'favorite_mode': 'casual',
            'achievements_count': 7
        },
        'frank': {
            'level': 15,
            'total_score': 8359,
            'sessions_played': 85,
            'favorite_mode': 'competitive',
            'achievements_count': 1
        }
    },
    'sessions': [
        {
            'player': 'bob',
            'duration_minutes': 94,
            'score': 1831,
            'mode': 'competitive',
            'completed': False
        },
        {
            'player': 'bob',
            'duration_minutes': 32,
            'score': 1478,
            'mode': 'casual',
            'completed': True
        },
        {
            'player': 'diana',
            'duration_minutes': 17,
            'score': 1570,
            'mode': 'competitive',
            'completed': False
        },
        {
            'player': 'alice',
            'duration_minutes': 98,
            'score': 1981,
            'mode': 'ranked',
            'completed': True
        },
        {
            'player': 'diana',
            'duration_minutes': 15,
            'score': 2361,
            'mode': 'competitive',
            'completed': False
        },
        {
            'player': 'eve',
            'duration_minutes': 29,
            'score': 2985,
            'mode': 'casual',
            'completed': True
        },
        {
            'player': 'frank',
            'duration_minutes': 34,
            'score': 1285,
            'mode': 'casual',
            'completed': True
        },
        {
            'player': 'alice',
            'duration_minutes': 53,
            'score': 1238,
            'mode': 'competitive',
            'completed': False
        },
        {
            'player': 'bob',
            'duration_minutes': 52,
            'score': 1555,
            'mode': 'casual',
            'completed': False
        },
        {
            'player': 'frank',
            'duration_minutes': 92,
            'score': 2754,
            'mode': 'casual',
            'completed': True
        },
        {
            'player': 'eve',
            'duration_minutes': 98,
            'score': 1102,
            'mode': 'casual',
            'completed': False
        },
        {
            'player': 'diana',
            'duration_minutes': 39,
            'score': 2721,
            'mode': 'ranked',
            'completed': True
        },
        {
            'player': 'frank',
            'duration_minutes': 46,
            'score': 329,
            'mode': 'casual',
            'completed': True
        },
        {
            'player': 'charlie',
            'duration_minutes': 56,
            'score': 1196,
            'mode': 'casual',
            'completed': True
        },
        {
            'player': 'eve',
            'duration_minutes': 117,
            'score': 1388,
            'mode': 'casual',
            'completed': False
        },
        {
            'player': 'diana',
            'duration_minutes': 118,
            'score': 2733,
            'mode': 'competitive',
            'completed': True
        },
        {
            'player': 'charlie',
            'duration_minutes': 22,
            'score': 1110,
            'mode': 'ranked',
            'completed': False
        },
        {
            'player': 'frank',
            'duration_minutes': 79,
            'score': 1854,
            'mode': 'ranked',
            'completed': False
        },
        {
            'player': 'charlie',
            'duration_minutes': 33,
            'score': 666,
            'mode': 'ranked',
            'completed': False
        },
        {
            'player': 'alice',
            'duration_minutes': 101,
            'score': 292,
            'mode': 'casual',
            'completed': True
        },
        {
            'player': 'frank',
            'duration_minutes': 25,
            'score': 2887,
            'mode': 'competitive',
            'completed': True
        },
        {
            'player': 'diana',
            'duration_minutes': 53,
            'score': 2540,
            'mode': 'competitive',
            'completed': False
        },
        {
            'player': 'eve',
            'duration_minutes': 115,
            'score': 147,
            'mode': 'ranked',
            'completed': True
        },
        {
            'player': 'frank',
            'duration_minutes': 118,
            'score': 2299,
            'mode': 'competitive',
            'completed': False
        },
        {
            'player': 'alice',
            'duration_minutes': 42,
            'score': 1880,
            'mode': 'casual',
            'completed': False
        },
        {
            'player': 'alice',
            'duration_minutes': 97,
            'score': 1178,
            'mode': 'ranked',
            'completed': True
        },
        {
            'player': 'eve',
            'duration_minutes': 18,
            'score': 2661,
            'mode': 'competitive',
            'completed': True
        },
        {
            'player': 'bob',
            'duration_minutes': 52,
            'score': 761,
            'mode': 'ranked',
            'completed': True
        },
        {
            'player': 'eve',
            'duration_minutes': 46,
            'score': 2101,
            'mode': 'casual',
            'completed': True
        },
        {
            'player': 'charlie',
            'duration_minutes': 117,
            'score': 1359,
            'mode': 'casual',
            'completed': True
        }
    ],
    'game_modes': ['casual', 'competitive', 'ranked'],
    'achievements': [
        'first_blood', 'level_master', 'speed_runner', 'treasure_seeker',
        'boss_hunter', 'pixel_perfect', 'first_blood', 'explorer'
    ]
}


def ListComp():
    hight_score = [
                    player
                    for player, data in data_list['players'].items()
                    if data['total_score'] > 2000
                    ]
    print("High scorers (>2000):", hight_score)

    score_double = [
                    data['total_score'] * 2
                    for data in data_list['players'].values()
                    ]
    print("Scores doubled:", score_double)

    active_player = list({
                          data['player']
                          for data in data_list['sessions']
                        })
    print("Active players:", sorted(active_player))


def DictComp():
    player_score = {
                    key: value['total_score']
                    for (key, value) in data_list['players'].items()
                    }
    print("Player scores:", player_score)

    score_categories = {
        'high': len([s for s in player_score.values() if s >= 2000]),
        'medium': len([s for s in player_score.values() if s >= 1000]),
        'low': len([s for s in player_score.values() if s <= 1000]),
    }
    print("Score categories:", score_categories)

    achiev_count = {
                    key: value['achievements_count']
                    for (key, value) in data_list['players'].items()
                    }
    print("Achievement counts:", achiev_count)


def SetComp():
    unique_player = {
                    player
                    for player in data_list['players']
                    }
    print("Unique players:", sorted(unique_player))

    unique_achievement = {
        achiev
        for achiev in data_list['achievements']
    }
    print("Unique achievements:", unique_achievement)

    active_regions = {
        region['mode']
        for region in data_list['sessions']
    }
    print("Active modes:", active_regions)


def CombiAnalysis():
    total_player = {
        data['player']
        for data in data_list['sessions']
    }
    print("Total players:", len(total_player))

    total_achiev = {
        achiev
        for achiev in data_list['achievements']
    }
    print("Total unique achievements:", len(total_achiev))

    average_score = (
        sum(s['total_score'] for s in data_list['players'].values())
        / len(data_list['players'])
    )
    print(f"Average score: {average_score:.1f}")

    top_perform = {
        key: (value['total_score'], value['achievements_count'])
        for (key, value) in data_list['players'].items()
        if value['total_score'] ==
        max(s['total_score'] for s in data_list['players'].values())
    }
    for name, (score, ach) in top_perform.items():
        print(f"Top performer: {name} ({score} points, {ach} achievements)")


def main():
    print("=== Game Analytics Dashboard ===")

    print("\n=== List Comprehension Examples ===")
    ListComp()

    print("\n=== Dict Comprehension Examples ===")
    DictComp()

    print("\n=== Set Comprehension Examples ===")
    SetComp()

    print("\n=== Combined Analysis ===")
    CombiAnalysis()


main()
