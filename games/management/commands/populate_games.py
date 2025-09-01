from django.core.management.base import BaseCommand
from games.models import GameCategory, Game


class Command(BaseCommand):
    help = 'Populate the database with initial games and categories'

    def handle(self, *args, **options):
        self.stdout.write('Creating game categories...')
        
        # Create categories
        categories_data = [
            {
                'name': 'RPG',
                'name_ar': 'آر بي جي',
                'description': 'Role-playing games that teach programming through adventures',
                'description_ar': 'ألعاب تمثيل الأدوار التي تعلم البرمجة من خلال المغامرات',
                'icon': 'rocket'
            },
            {
                'name': 'Creative',
                'name_ar': 'إبداعي',
                'description': 'Creative games for building and designing',
                'description_ar': 'ألعاب إبداعية للبناء والتصميم',
                'icon': 'puzzle-piece'
            },
            {
                'name': 'Puzzle',
                'name_ar': 'ألغاز',
                'description': 'Logic and problem-solving games',
                'description_ar': 'ألعاب المنطق وحل المشاكل',
                'icon': 'robot'
            },
            {
                'name': 'Adventure',
                'name_ar': 'مغامرة',
                'description': 'Adventure games with coding challenges',
                'description_ar': 'ألعاب مغامرة مع تحديات البرمجة',
                'icon': 'gamepad'
            },
            {
                'name': 'Space',
                'name_ar': 'فضاء',
                'description': 'Space exploration and programming',
                'description_ar': 'استكشاف الفضاء والبرمجة',
                'icon': 'rocket'
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = GameCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        self.stdout.write('Creating games...')
        
        # Create games based on the frontend data
        games_data = [
            {
                'title': 'Code Combat',
                'title_ar': 'معركة البرمجة',
                'description': 'Learn programming through epic RPG adventures! Battle monsters and solve quests using real code.',
                'description_ar': 'تعلم البرمجة من خلال مغامرات آر بي جي ملحمية! حارب الوحوش وحل المهام باستخدام كود حقيقي.',
                'duration_minutes': 45,
                'difficulty': 'intermediate',
                'total_levels': 15,
                'category': categories['RPG'],
                'skills': ['Python', 'JavaScript', 'Problem Solving'],
                'rating': 4.8,
                'player_count': '1.2M+',
                'is_featured': True,
                'order': 1
            },
            {
                'title': 'Scratch Jr Adventures',
                'title_ar': 'مغامرات سكراتش الصغير',
                'description': 'Create interactive stories and games with colorful blocks! Perfect for young coders to start their journey.',
                'description_ar': 'أنشئ قصص وألعاب تفاعلية بكتل ملونة! مثالي للمبرمجين الصغار لبدء رحلتهم.',
                'duration_minutes': 30,
                'difficulty': 'beginner',
                'total_levels': 8,
                'category': categories['Creative'],
                'skills': ['Visual Programming', 'Storytelling', 'Animation'],
                'rating': 4.9,
                'player_count': '800K+',
                'is_featured': True,
                'order': 2
            },
            {
                'title': 'Robot Maze Challenge',
                'title_ar': 'تحدي متاهة الروبوت',
                'description': 'Guide your robot through challenging mazes using programming logic and algorithms!',
                'description_ar': 'وجه روبوتك عبر متاهات صعبة باستخدام منطق البرمجة والخوارزميات!',
                'duration_minutes': 35,
                'difficulty': 'beginner',
                'total_levels': 10,
                'category': categories['Puzzle'],
                'skills': ['Algorithms', 'Logic', 'Problem Solving'],
                'rating': 4.7,
                'player_count': '650K+',
                'order': 3
            },
            {
                'title': 'Code Monkey Island',
                'title_ar': 'جزيرة القرد المبرمج',
                'description': 'Help the monkey collect bananas by writing code! Learn loops, functions, and variables in a tropical paradise.',
                'description_ar': 'ساعد القرد في جمع الموز بكتابة الكود! تعلم الحلقات والوظائف والمتغيرات في جنة استوائية.',
                'duration_minutes': 40,
                'difficulty': 'beginner',
                'total_levels': 12,
                'category': categories['Adventure'],
                'skills': ['Loops', 'Functions', 'Variables'],
                'rating': 4.6,
                'player_count': '950K+',
                'order': 4
            },
            {
                'title': 'Pixel Art Creator',
                'title_ar': 'منشئ فن البكسل',
                'description': 'Create amazing pixel art while learning about coordinates, loops, and digital art concepts!',
                'description_ar': 'أنشئ فن بكسل مذهل أثناء تعلم الإحداثيات والحلقات ومفاهيم الفن الرقمي!',
                'duration_minutes': 50,
                'difficulty': 'intermediate',
                'total_levels': 14,
                'category': categories['Creative'],
                'skills': ['Coordinates', 'Art', 'Loops'],
                'rating': 4.5,
                'player_count': '420K+',
                'order': 5
            },
            {
                'title': 'Space Code Explorer',
                'title_ar': 'مستكشف كود الفضاء',
                'description': 'Navigate through space while learning advanced programming concepts! Build rockets and explore galaxies.',
                'description_ar': 'تنقل عبر الفضاء أثناء تعلم مفاهيم البرمجة المتقدمة! ابني صواريخ واستكشف المجرات.',
                'duration_minutes': 60,
                'difficulty': 'advanced',
                'total_levels': 18,
                'category': categories['Space'],
                'skills': ['Advanced Logic', 'Physics', 'Game Development'],
                'rating': 4.9,
                'player_count': '320K+',
                'is_featured': True,
                'order': 6
            }
        ]
        
        for game_data in games_data:
            game, created = Game.objects.get_or_create(
                title=game_data['title'],
                defaults=game_data
            )
            if created:
                self.stdout.write(f'Created game: {game.title}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated {GameCategory.objects.count()} categories '
                f'and {Game.objects.count()} games'
            )
        )
