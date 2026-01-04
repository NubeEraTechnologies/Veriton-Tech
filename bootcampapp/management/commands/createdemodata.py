from django.core.management.base import BaseCommand
from bootcampapp import models as MyModels
import random

class Command(BaseCommand):
    help = 'Create a Demo schools and grades'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Creating Schools...'))
        for i in range (1):
            self.stdout.write(self.style.NOTICE(f'Creating School {i}'))
            MyModels.School.objects.create(
                school_name = f'School {i}',
                contact_person = f'Sir {i}',
                email = 'email@mailservice.com',
                address = 'School address',
                phone_number = '1234567890'
            ).save()
        self.stdout.write(self.style.SUCCESS('Schools created successfully...'))
        self.stdout.write(self.style.NOTICE('Creating Grades...'))
        
        MyModels.Grade.objects.create(
                grade_name = 'V',
            ).save()
        
        MyModels.Grade.objects.create(
                grade_name = 'VI',
            ).save()
        
        MyModels.Grade.objects.create(
                grade_name = 'VII',
            ).save()
        
        MyModels.Grade.objects.create(
                grade_name = 'VIII',
            ).save()
        
        MyModels.Grade.objects.create(
                grade_name = 'IX',
            ).save()
        self.stdout.write(self.style.SUCCESS('Grades created successfully...'))

        
        self.stdout.write(self.style.NOTICE('Creating Divisions...'))
                
        MyModels.Division.objects.create(
                division_name = 'A',
            ).save()
        
        MyModels.Division.objects.create(
                division_name = 'B',
            ).save()
        
        MyModels.Division.objects.create(
                division_name = 'C',
            ).save()
        
        MyModels.Division.objects.create(
                division_name = 'D',
            ).save()
        
        MyModels.Division.objects.create(
                division_name = 'E',
            ).save()
        MyModels.Division.objects.create(
                division_name = 'F',
            ).save()
        MyModels.Division.objects.create(
                division_name = 'G',
            ).save()
        MyModels.Division.objects.create(
                division_name = 'H',
            ).save()
        MyModels.Division.objects.create(
                division_name = 'I',
            ).save()

        self.stdout.write(self.style.SUCCESS('Divisions created successfully...'))

        # self.stdout.write(self.style.NOTICE('Creating Modules...'))
        # for i in range (5):
        #     self.stdout.write(self.style.NOTICE(f'Creating Module {i +1}'))
        #     MyModels.Module.objects.create(
        #         grade_id = 1,
        #         module_name = f'Module {i +1}',
        #         description = f'Description {i +1}',
        #     ).save()
        
        # for i in range (5):
        #     self.stdout.write(self.style.NOTICE(f'Creating Module {i + 50}'))
        #     MyModels.Module.objects.create(
        #         grade_id = 2,
        #         module_name = f'Module {i + 50}',
        #         description = f'Description {i+50}',
        #     ).save()

        # for i in range (5):
        #     self.stdout.write(self.style.NOTICE(f'Creating Module {i +100}'))
        #     MyModels.Module.objects.create(
        #         grade_id = 3,
        #         module_name = f'Module {i + 100}',
        #         description = f'Description {i+100}',
        #     ).save()
        # self.stdout.write(self.style.SUCCESS('Module created successfully...'))

        # self.stdout.write(self.style.NOTICE('Creating Lessons...'))
        # video_ids = [
        #     "e6MhFghdQps",
        #     "3JZ_D3ELwOQ",
        #     "L_jWHffIx5E",
        #     "kJQP7kiw5Fk",
        #     "tgbNymZ7vqY",
        #     "oHg5SJYRHA0",
        #     "2Vv-BfVoq4g",
        #     "9bZkp7q19f0",
        #     "CevxZvSJLk8",
        #     "3fumBcKC6RE",
        #     "6hUQ0G_Po1o",
        #     "a_426R_1Sh8",
        #     "8UVNT4wvIGY",
        #     "0KSOMA3QBU0",
        #     "KQ6zrB4ATcI",
        #     "9Sc-ir4HcBk",
        #     "gGdGFZ0Xr0I",
        #     "hY7m5jjJ9mI",
        #     "P2sS2e4n07I",
        #     "6fVQhF9wRe0",
        #     "ftX9a5WXXEo",
        #     "zWjVoD1pR6U",
        #     "B8z9YZg1IV8",
        #     "YBHQbv_95Y0",
        #     "4f0tOmtXk2M"
        # ]
        # for i in range (10):
        #     self.stdout.write(self.style.NOTICE(f'Creating Lesson {i +1} as heading {i +1}'))
        #     MyModels.Lesson.objects.create(
        #         grade_id = 1,
        #         module_id = 1,
        #         serialno = i +1,
        #         mints = 60,
        #         heading = f'Heading {i+1}',
        #         about = ' <div class="mb-4">\
        #         <h3 class="text-success">About STEAM and IoT</h3>\
        #         <p>\
        #             <strong>STEAM education</strong> integrates Science, Technology, Engineering, Arts, and Mathematics to foster creativity and critical thinking. IoT, or the <strong>Internet of Things</strong>, is the concept of connecting everyday devices to the internet to collect and share data. In this lesson, we will explore how STEAM can be applied through hands-on learning with IoT and Arduino technology.\
        #         </p>\
        #         <img src="images/steam_iot.jpg" class="img-fluid" alt="STEAM and IoT Image">\
        #         </div>',

        #         reqmaterial ='<div class="mb-4">\
        #                     <h3 class="text-success">Required Materials</h3>\
        #                     <ul class="list-group">\
        #                         <li class="list-group-item">1x Arduino UNO</li>\
        #                         <li class="list-group-item">1x ESP8266 Wi-Fi Module</li>\
        #                         <li class="list-group-item">Jumper Wires</li>\
        #                         <li class="list-group-item">Breadboard</li>\
        #                         <li class="list-group-item">LED, Resistors</li>\
        #                     </ul>\
        #                 </div>',
        #             video = random.choice(video_ids),
        #             digram = 'https://ai.thestempedia.com/wp-content/uploads/2023/05/DC_Motor_fritzing_bb-e1579694616737-1.png',
        #             code = 'https://ai.thestempedia.com/wp-content/uploads/2023/05/Chapter7_UploadFirmware-3.sb2',
        #             process = '<div class="mb-4">\
        #                     <h3 class="text-success">Procedure</h3>\
        #                     <ol class="list-group list-group-numbered">\
        #                         <li class="list-group-item">Connect the Arduino to the Wi-Fi module using jumper wires as per the circuit diagram.</li>\
        #                         <li class="list-group-item">Upload the provided code to your Arduino using the Arduino IDE.</li>\
        #                         <li class="list-group-item">Open the serial monitor to view connection status.</li>\
        #                         <li class="list-group-item">Once connected, you can send and receive data over the internet.</li>\
        #                     </ol>\
        #                 </div>',
        #             get = '<p>&lt;div class=&quot;mb-4&quot;&gt; &lt;h3 class=&quot;text-success&quot;&gt;What You Get&lt;/h3&gt; &lt;p&gt;By completing this lesson, you will learn how to set up a basic IoT system using Arduino and ESP8266. You will understand how devices communicate over Wi-Fi and how to program simple IoT applications.&lt;/p&gt; &lt;/div&gt;</p>'
        #     ).save()

        # for i in range (10):
        #     self.stdout.write(self.style.NOTICE(f'Creating Lesson {i +12} as heading {i +12}'))
        #     MyModels.Lesson.objects.create(
        #         grade_id = 1,
        #         module_id = 2,
        #         serialno = i +1,
        #         mints = 60,
        #         heading = f'Heading {i+12}',
        #         about = ' <div class="mb-4">\
        #         <h3 class="text-success">About STEAM and IoT</h3>\
        #         <p>\
        #             <strong>STEAM education</strong> integrates Science, Technology, Engineering, Arts, and Mathematics to foster creativity and critical thinking. IoT, or the <strong>Internet of Things</strong>, is the concept of connecting everyday devices to the internet to collect and share data. In this lesson, we will explore how STEAM can be applied through hands-on learning with IoT and Arduino technology.\
        #         </p>\
        #         <img src="images/steam_iot.jpg" class="img-fluid" alt="STEAM and IoT Image">\
        #         </div>',

        #         reqmaterial ='<div class="mb-4">\
        #                     <h3 class="text-success">Required Materials</h3>\
        #                     <ul class="list-group">\
        #                         <li class="list-group-item">1x Arduino UNO</li>\
        #                         <li class="list-group-item">1x ESP8266 Wi-Fi Module</li>\
        #                         <li class="list-group-item">Jumper Wires</li>\
        #                         <li class="list-group-item">Breadboard</li>\
        #                         <li class="list-group-item">LED, Resistors</li>\
        #                     </ul>\
        #                 </div>',
        #             video = random.choice(video_ids),
        #             digram = 'https://ai.thestempedia.com/wp-content/uploads/2023/05/DC_Motor_fritzing_bb-e1579694616737-1.png',
        #             code = 'https://ai.thestempedia.com/wp-content/uploads/2023/05/Chapter7_UploadFirmware-3.sb2',
        #             process = '<div class="mb-4">\
        #                     <h3 class="text-success">Procedure</h3>\
        #                     <ol class="list-group list-group-numbered">\
        #                         <li class="list-group-item">Connect the Arduino to the Wi-Fi module using jumper wires as per the circuit diagram.</li>\
        #                         <li class="list-group-item">Upload the provided code to your Arduino using the Arduino IDE.</li>\
        #                         <li class="list-group-item">Open the serial monitor to view connection status.</li>\
        #                         <li class="list-group-item">Once connected, you can send and receive data over the internet.</li>\
        #                     </ol>\
        #                 </div>',
        #             get = '<p>&lt;div class=&quot;mb-4&quot;&gt; &lt;h3 class=&quot;text-success&quot;&gt;What You Get&lt;/h3&gt; &lt;p&gt;By completing this lesson, you will learn how to set up a basic IoT system using Arduino and ESP8266. You will understand how devices communicate over Wi-Fi and how to program simple IoT applications.&lt;/p&gt; &lt;/div&gt;</p>'
        #     ).save()
        
        # for i in range (10):
        #     self.stdout.write(self.style.NOTICE(f'Creating Lesson {i +32} as heading {i +32}'))
        #     MyModels.Lesson.objects.create(
        #         grade_id = 1,
        #         module_id = 3,
        #         serialno = i +1,
        #         mints = 60,
        #         heading = f'Heading {i+32}',
        #         about = ' <div class="mb-4">\
        #         <h3 class="text-success">About STEAM and IoT</h3>\
        #         <p>\
        #             <strong>STEAM education</strong> integrates Science, Technology, Engineering, Arts, and Mathematics to foster creativity and critical thinking. IoT, or the <strong>Internet of Things</strong>, is the concept of connecting everyday devices to the internet to collect and share data. In this lesson, we will explore how STEAM can be applied through hands-on learning with IoT and Arduino technology.\
        #         </p>\
        #         <img src="images/steam_iot.jpg" class="img-fluid" alt="STEAM and IoT Image">\
        #         </div>',

        #         reqmaterial ='<div class="mb-4">\
        #                     <h3 class="text-success">Required Materials</h3>\
        #                     <ul class="list-group">\
        #                         <li class="list-group-item">1x Arduino UNO</li>\
        #                         <li class="list-group-item">1x ESP8266 Wi-Fi Module</li>\
        #                         <li class="list-group-item">Jumper Wires</li>\
        #                         <li class="list-group-item">Breadboard</li>\
        #                         <li class="list-group-item">LED, Resistors</li>\
        #                     </ul>\
        #                 </div>',
        #             video = random.choice(video_ids),
        #             digram = 'https://ai.thestempedia.com/wp-content/uploads/2023/05/DC_Motor_fritzing_bb-e1579694616737-1.png',
        #             code = 'https://ai.thestempedia.com/wp-content/uploads/2023/05/Chapter7_UploadFirmware-3.sb2',
        #             process = '<div class="mb-4">\
        #                     <h3 class="text-success">Procedure</h3>\
        #                     <ol class="list-group list-group-numbered">\
        #                         <li class="list-group-item">Connect the Arduino to the Wi-Fi module using jumper wires as per the circuit diagram.</li>\
        #                         <li class="list-group-item">Upload the provided code to your Arduino using the Arduino IDE.</li>\
        #                         <li class="list-group-item">Open the serial monitor to view connection status.</li>\
        #                         <li class="list-group-item">Once connected, you can send and receive data over the internet.</li>\
        #                     </ol>\
        #                 </div>',
        #             get = '<p>&lt;div class=&quot;mb-4&quot;&gt; &lt;h3 class=&quot;text-success&quot;&gt;What You Get&lt;/h3&gt; &lt;p&gt;By completing this lesson, you will learn how to set up a basic IoT system using Arduino and ESP8266. You will understand how devices communicate over Wi-Fi and how to program simple IoT applications.&lt;/p&gt; &lt;/div&gt;</p>'
        #     ).save()
        
        # self.stdout.write(self.style.SUCCESS('Lessons created successfully...'))
        # self.stdout.write(self.style.NOTICE('Creating Questions...'))

        # for i in range (25):
        #     self.stdout.write(self.style.NOTICE(f'Creating Module Question {i +1} '))
        #     MyModels.ModuleQuestion.objects.create(
        #         grade_id = 1,
        #         module_id = 1,
        #         question = f'Question {i + 1}',
        #         option1='option1',
        #         option2='option2',
        #         option3='option3',
        #         option4='option4',
        #         answer= str(random.randint(1, 4)),
        #         marks=1
        #     ).save()

        # for i in range (25):
        #     self.stdout.write(self.style.NOTICE(f'Creating Module Question {i +20} '))
        #     MyModels.ModuleQuestion.objects.create(
        #         grade_id = 1,
        #         module_id = 2,
        #         question = f'Question {i + 20}',
        #         option1='option1',
        #         option2='option2',
        #         option3='option3',
        #         option4='option4',
        #         answer= str(random.randint(1, 4)),
        #         marks=1
        #     ).save()

        # for i in range (25):
        #     self.stdout.write(self.style.NOTICE(f'Creating Module Question {i +20} '))
        #     MyModels.ModuleQuestion.objects.create(
        #         grade_id = 1,
        #         module_id = 3,
        #         question = f'Question {i + 20}',
        #         option1='option1',
        #         option2='option2',
        #         option3='option3',
        #         option4='option4',
        #         answer= str(random.randint(1, 4)),
        #         marks=1
        #     ).save()

        # self.stdout.write(self.style.SUCCESS('Questions created successfully...'))
        