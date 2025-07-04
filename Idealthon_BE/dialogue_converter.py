import csv
import re


def convert_dialogue_to_csv(text_data, output_csv_file):
    """
    Chuyển đổi dữ liệu đoạn hội thoại từ định dạng văn bản sang CSV.

    Args:
        text_data (str): Chuỗi chứa toàn bộ dữ liệu đoạn hội thoại với dấu thời gian.
        output_csv_file (str): Tên file CSV đầu ra.
    """
    lines = text_data.strip().split('\n')

    # Biểu thức chính quy để tìm dấu thời gian và lời nói
    # Nó tìm kiếm một mẫu <time>X.XX</time> theo sau là bất kỳ ký tự nào cho đến hết dòng.
    pattern = re.compile(r'<time>(\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2})</time>\s*(.*)')

    data_for_csv = []

    for line in lines:
        match = pattern.match(line)
        if match:
            timestamp_str = match.group(1)
            speaker_text = match.group(2).strip()  # Lấy phần lời nói và loại bỏ khoảng trắng thừa

            # Bạn có thể thêm logic để phân biệt người nói nếu có mẫu rõ ràng (ví dụ: "Natalie:", "John:")
            # Hiện tại, chúng ta sẽ đặt người nói là 'Unknown' hoặc trích xuất nếu có trong lời nói.

            # Đối với dữ liệu ví dụ của bạn, không có tên người nói rõ ràng trên mỗi dòng
            # nên chúng ta có thể đặt một cột 'Content' duy nhất.
            data_for_csv.append({'timestamp': timestamp_str, 'transcript': speaker_text})
        else:
            print(f"Bỏ qua dòng không khớp định dạng: {line}")

    # Ghi dữ liệu vào file CSV
    try:
        with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['timestamp', 'transcript']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()  # Ghi tiêu đề cột
            writer.writerows(data_for_csv)  # Ghi dữ liệu

        print(f"Dữ liệu đã được chuyển đổi và lưu vào '{output_csv_file}' thành công!")
    except IOError as e:
        print(f"Lỗi khi ghi file CSV: {e}")


# --- Dữ liệu đầu vào của bạn ---
dialogue_text = """<time>0:00 - 0:05</time> 2 1 bắt đầu.
<time>0:05 - 0:17</time> When I got the news that I be going to friend to meet and work with our client in person, I was super excited.
<time>0:18 - 0:30</time> It was not only a promising experiences in a country far from my hometown bị mở mất chữ rồi, không nhìn thấy chữ gì.
<time>0:30 - 0:32</time> Dừng đến what's excited thôi.
<time>0:33 - 0:33</time> Thế dừng à?
<time>0:33 - 0:34</time> Dừng thôi.
<time>0:34 - 0:38</time> Dừng xong anh ấy lại 1 2 3 xong lại tiếp à?
<time>0:38 - 0:40</time> À, một câu xong dừng gì không?
<time>0:41 - 0:43</time> 3 2 1 bắt đầu.
<time>0:45 - 0:53</time> When I got the news that I be going to friend to meet and work with our client in person.
<time>0:57 - 1:00</time> 3 2 1 bắt đầu.
<time>1:00 - 1:08</time> When I got the news that I be going to friend to meet and work with our client in person, I was super excited.
<time>1:11 - 1:13</time> Ok.
<time>1:13 - 1:13</time> 2 1 bắt đầu.
<time>1:15 - 1:19</time> It was not
<time>1:20 - 1:21</time> Bọn nói hết rồi.
<time>1:28 - 1:36</time> It was not only a promising appearances in a country far from my homeland of Vietnam, but it was also a reverse for my efforts.
<time>1:43 - 1:45</time> 3 2 1 bắt đầu.
<time>1:46 - 1:56</time> It was not only a promising experiences in a country far from my homeland of Vietnam, but it was also a reverse for my efforts.
<time>1:59 - 2:00</time> Ok.
<time>2:01 - 2:03</time> đẹp đấy.
<time>2:03 - 2:06</time> 3 2 1 bắt đầu.
<time>2:08 - 2:20</time> Hi, I'm Dương, a senior engineer with 5 year on Rabylo.
<time>2:20 - 2:21</time> quên rồi.
<time>2:22 - 2:26</time> 5 years senior Rabylo.
<time>2:26 - 2:28</time> 2 1 bắt đầu.
<time>2:29 - 2:34</time> Hi, I'm Dương, a senior engineer with 5 years at Rabylo.
<time>2:38 - 2:39</time> Ok.
<time>2:44 - 2:45</time> đẹp đấy.
<time>2:46 - 2:46</time> 2 1 bắt đầu.
<time>2:48 - 2:56</time> Hi, I'm Dương, a senior engineer with 5 years at Rabylo.
<time>2:58 - 3:06</time> My motto is still passionate.
<time>3:06 - 3:07</time> Still passionate.
<time>3:07 - 3:11</time> Always moving forward.
<time>3:12 - 3:12</time> Ok, lại nha.
<time>3:13 - 3:14</time> Still passionate.
<time>3:14 - 3:16</time> 2 1 bắt đầu.
<time>3:19 - 3:26</time> Hi, I'm Dương, a senior a senior engineer.
<time>3:26 - 3:27</time> Lại lại lại lại.
<time>3:33 - 3:34</time> 2 1.
<time>3:37 - 3:51</time> Hi, I'm Dương, a senior engineer with 5 year at Rabylo.
<time>3:51 - 3:55</time> My motto is.
<time>3:59 - 4:00</time> bắt đầu.
<time>4:02 - 4:09</time> Hi, I'm Dương, a senior engineer with 5 years at Rabylo.
<time>4:09 - 4:10</time> My motto is.
<time>4:11 - 4:13</time> always moving.
<time>4:13 - 4:15</time> still passionate.
<time>4:16 - 4:18</time> Ơ, nói tiếp từ cái mà motto đúng không?
<time>4:19 - 4:20</time> ừ, tôi nói liền luôn.
<time>4:20 - 4:21</time> My motto is.
<time>4:25 - 4:25</time> hay là phải nói từ đầu ấy?
<time>4:26 - 4:26</time> Nói từ đầu chứ.
<time>4:27 - 4:27</time> Okay.
<time>4:27 - 4:28</time> Nói luôn.
<time>4:31 - 4:35</time> Sorry.
<time>4:37 - 4:38</time> 2 1 bắt đầu.
<time>4:40 - 4:48</time> Hi, I'm Dương, a senior engineer with 5 years at Rabylo.
<time>4:48 - 4:52</time> My motto is.
<time>4:53 - 5:01</time> still passionate, always moving forward.
<time>5:04 - 5:05</time> Ok.
<time>5:07 - 5:08</time> căng thẳng quá.
<time>5:09 - 5:10</time> 2 1 bắt đầu.
<time>5:13 - 5:20</time> My father is a mechanical engineer, I lại and I have been tinkering.
<time>5:21 - 5:24</time> Lại nha.
<time>5:25 - 5:25</time> cái này I have been, không phải I have been.
<time>5:26 - 5:26</time> À, với cả cái này nhá.
<time>5:27 - 5:28</time> 1
<time>5:28 - 5:29</time> bắt đầu.
<time>5:30 - 5:42</time> My father is a mechanical engineer and I has been tinkering with his work tools since I were very young.
<time>5:42 - 5:50</time> That sparked my fascination with the world of machines, computer and logics.
<time>5:50 - 5:55</time> Becoming a software engineer has been my dream.
<time>5:57 - 5:58</time> Lại thêm một bạn nữa đi.
<time>5:58 - 6:00</time> Nó có bị cao quá.
<time>6:01 - 6:03</time> Em, em đang bị, sẽ bị nâng ở đoạn cuối.
<time>6:03 - 6:06</time> Has been my dream.
<time>6:09 - 6:10</time> Lại nha.
<time>6:13 - 6:20</time> My father is a my father is mechanical engineer.
<time>6:20 - 6:21</time> Lại lại lại.
<time>6:21 - 6:27</time> My father is a mechanical engineer and I haven't tinkering with his work tools since I was very young.
<time>6:27 - 6:35</time> That sparked my fascination with the world of machines, computer and logic.
<time>6:35 - 6:39</time> Becoming a software engineer has been my dream.
<time>6:41 - 6:41</time> Ok đấy.
<time>6:45 - 6:52</time> Ở cái giọng này bạn ấy nói nhỏ hơn so với lúc vừa nãy thì anh tăng.
<time>6:52 - 6:53</time> 2 1 bắt đầu.
<time>6:54 - 7:03</time> When I was student in the Hà Nội University of Technology, I had the chance to listen to Cường, the CEO of Rabylo.
<time>7:03 - 7:04</time> tại sao lại thiếu lại lại em ạ.
<time>7:04 - 7:05</time> to Mr. Cường.
<time>7:06 - 7:06</time> Ơ, hôm qua có Mr. Cường mà.
<time>7:11 - 7:12</time> Bắt đầu nha anh nhá.
<time>7:15 - 7:24</time> When I was student in the Hà Nội University of Technology, I had the chance to listen to Mr. Cường.
<time>7:28 - 7:30</time> to listen to Mr. Cường, nghe thôi.
<time>7:30 - 7:31</time> Đúng chưa ạ?
<time>7:33 - 7:35</time> I had the chance to meet.
<time>7:35 - 7:41</time> the chance to to meet to meet Mr. Cường.
<time>7:41 - 7:41</time> To meet Mr. Cường.
<time>7:46 - 7:47</time> Mr.
<time>7:47 - 7:47</time> Mr. Cường.
<time>7:50 - 7:51</time> To meet the.
<time>7:51 - 7:52</time> To meet Mr. Cường.
<time>7:54 - 7:55</time> To meet.
<time>7:55 - 7:56</time> to meet.
<time>8:00 - 8:09</time> When I was student in the Hà Nội University of Technology, I had a chance to meet Mr. Cường, the CEO of Rabylo.
<time>8:09 - 8:16</time> who is also an alumnus of the university share his inspiring startup journey started from an employee in Japan.
<time>8:16 - 8:23</time> Then back to startup in Vietnam and build a bridge of technology talents between Vietnam and Japan.
<time>8:23 - 8:24</time> Đọc lại câu này nhá.
<time>8:25 - 8:26</time> Okay.
<time>8:27 - 8:38</time> Started from started from an employee in Japan, then back to startup in Vietnam and build a bridge of technology talents between Vietnam and Japan.
<time>8:39 - 8:43</time> Nhưng mà đoạn này giọng điệu nó hơi bị đọc quá hay sao đấy?
<time>8:43 - 8:44</time> Giọng này nó đang hơi bị.
<time>8:44 - 8:47</time> Cái này phải đọc, cái này phải giống nói.
<time>8:47 - 8:56</time> Ờ, có lúc đọc vẫn giống như kiểu là em đang nói chuyện với chị ấy.
<time>8:56 - 8:58</time> Started from.
<time>8:58 - 9:00</time> khi kể When I was a student in the Hà Nội University.
<time>9:00 - 9:01</time> 3 2 1 bắt đầu.
<time>9:02 - 9:15</time> When I was student in the Hà Nội University of Technology, I had a chance to meet Mr. Cường, the CEO of Rabylo, who is also an alumnus of the university share his inspiring startup journey.
<time>9:16 - 9:21</time> Started from an employee in Japan, then back to
<time>9:21 - 9:23</time> Startup in Vietnam and build.
<time>9:23 - 9:24</time> Không hợp lý lắm nhỉ.
<time>9:29 - 9:30</time> Cũng được.
<time>9:31 - 9:31</time> Tiếp ha.
<time>9:31 - 9:32</time> Tại vì đoạn sau vẫn là.
<time>9:33 - 9:33</time> 2 1 bắt đầu.
<time>9:35 - 9:41</time> Started from an employee in Japan, then back to startup in Vietnam and build a bridge of technology talents between Vietnam and Japan,
<time>9:41 - 9:44</time> his story and the mission of bringing Vietnamese technological expertise to contribute to global.
<time>9:44 - 9:46</time> như đọc đấy nhỉ.
<time>9:47 - 9:48</time> To contribute to global.
<time>9:48 - 9:49</time> Lại.
<time>9:50 - 10:01</time> started from an employee in Japan, then back to startup in Vietnam and build a bridge of technology talents between Vietnam and Japan, his story and the mission of bringing Vietnamese technological expertise to contribute to global sustainable development.
<time>10:04 - 10:05</time> kiểu gì ấy.
<time>10:07 - 10:09</time> quá đúng không.
<time>10:09 - 10:11</time> Okay chị.
<time>10:11 - 10:13</time> Để em xem ngắt nghỉ ở đâu.
<time>10:13 - 10:14</time> Chúng ta có đoạn mà.
<time>10:16 - 10:17</time> 2 1 bắt đầu.
<time>10:17 - 10:26</time> his story and the mission of
<time>10:27 - 10:27</time> 2 1 bắt đầu.
<time>10:29 - 10:36</time> His story and the mission of bringing Vietnamese software engineer to contribute to global sustainable development.
<time>10:36 - 10:37</time> Lại lại lại.
<time>10:38 - 10:45</time> development.
<time>10:45 - 10:46</time> 3 2 1 bắt đầu.
<time>10:46 - 10:54</time> His story and the mission of bringing Vietnamese software engineer to contribute to global sustainable development.
<time>10:55 - 10:56</time> Ơ, em nhìn vào cái camera rồi.
<time>10:57 - 11:00</time> Tự nhiên lại nhìn được cái camera.
<time>11:00 - 11:00</time> Hello.
<time>11:00 - 11:01</time> Lại nha.
<time>11:04 - 11:12</time> His story and the mission of bringing Vietnamese software engineer to contribute to global sustainable development.
<time>11:14 - 11:15</time> Ok.
<time>11:16 - 11:16</time> 2 1 bắt đầu.
<time>11:18 - 11:21</time> Have motivated me to become a part of Rabylo, a true builder.
<time>11:23 - 11:24</time> Hình như đoạn này đọc không có hết rồi.
<time>11:25 - 11:25</time> có chút.
<time>11:26 - 11:26</time> Have.
<time>11:27 - 11:30</time> 3 2 1 bắt đầu.
<time>11:31 - 11:36</time> Have motivated me to become a part of Rabylo, a true builder.
<time>11:38 - 11:39</time> Ok.
<time>11:39 - 11:40</time> 19.
<time>11:41 - 11:42</time> 3 2 1 bắt đầu.
<time>11:43 - 11:53</time> When I set my mind to become a female software engineer, I understood that there would be certain difficulties that I need to overcome.
<time>11:54 - 12:05</time> The difficulties are not about expertise or gender inequality in the workplace for me, it were about balancing my career, family caregiving and health, especially when I were married.
<time>12:07 - 12:10</time> Không đọc lại thôi cái câu for me.
<time>12:12 - 12:20</time> For me, it was about balancing my career, family caregiving and health, especially when I was married.
<time>12:21 - 12:22</time> Nó bị vướng cái cửa đúng không?
<time>12:23 - 12:23</time> Ờ ok.
<time>12:24 - 12:25</time> 2 1 bắt đầu.
<time>12:26 - 12:35</time> There are many times when I have faced very clear physical limitation compared to my male colleagues on the project.
<time>12:38 - 12:39</time> Hình như là đoạn này hơi.
<time>12:39 - 12:40</time> 2 1 bắt đầu.
<time>12:42 - 12:50</time> There are many times when I have face with clear physical limitation compared to my male colleagues on the project.
<time>12:51 - 12:52</time> hơi vấp.
<time>12:52 - 12:52</time> hơi vấp đoạn này.
<time>12:53 - 12:59</time> There are many times, there are many times when I have face very clear physical limitation compared to my male colleagues on the project.
<time>13:04 - 13:04</time> 3 2.
<time>13:05 - 13:07</time> 2 1 bắt đầu.
<time>13:07 - 13:15</time> They are very lại lại.
<time>13:16 - 13:25</time> There are many moments when I plan to cook a special meal for my family myself, but the choice ended up eating out because I need time to rest after a hard working day.
<time>13:29 - 13:29</time> Ok.
<time>13:31 - 13:32</time> 3 2 1 bắt đầu.
<time>13:33 - 13:43</time> The project that brought me to friends is also a project I have been part of for over 2 years.
<time>13:45 - 13:46</time> hết một câu rồi.
<time>13:46 - 13:47</time> hết rồi à?
<time>13:47 - 13:50</time> Tưởng ý là vẫn còn, nhưng mà có đọc luôn hai câu không?
<time>13:52 - 13:54</time> 3 2 1 bắt đầu.
<time>13:54 - 14:03</time> The project that brought me to France, is also a project that I have been part of for over two years, it is truly impressive that I have been working at Rabylo for five years, right?
<time>14:06 - 14:06</time> Ok.
<time>14:06 - 14:08</time> Ok.
<time>14:09 - 14:10</time> 2 1 bắt đầu.
<time>14:10 - 14:14</time> When Mr. Kiên.
<time>14:16 - 14:18</time> When Mr. Kiên.
<time>14:18 - 14:20</time> cái giọng như nào thế nhỉ?
<time>14:20 - 14:21</time> Mr. Kiên.
<time>14:21 - 14:29</time> When Mr. Kiên, my direct manager Rabylo announce that I was selected to work in France.
<time>14:29 - 14:37</time> I was surprised, delighted and a little worry.
<time>14:37 - 14:46</time> Although it would be a great opportunity for me to meet talent engineers and expand my experiences in a developed country,
<time>14:46 - 14:51</time> I had to be away from my family for a period time.
<time>14:51 - 14:53</time> Many thing could happen.
<time>14:55 - 14:55</time> Lại một lần nữa nhá.
<time>14:56 - 14:58</time> hơi nhỏ nha.
<time>14:58 - 15:01</time> Em nói lại.
<time>15:01 - 15:02</time> Nhỏ à?
<time>15:02 - 15:05</time> Vừa nãy thì chị thấy cái cái cảm xúc thì ok rồi nhá.
<time>15:05 - 15:06</time> Kiên.
<time>15:07 - 15:08</time> Lại nha.
<time>15:10 - 15:18</time> When Mr. Kiên, my direct thể cái chữ Kiên này khó đọc.
<time>15:19 - 15:21</time> When Mr. Kiên,
<time>15:21 - 15:22</time> chị, chị ấy mớm lại xem nào.
<time>15:22 - 15:24</time> When Mr. Kiên.
<time>15:24 - 15:26</time> When Mr. Kiên?
<time>15:27 - 15:27</time> when Mr. Kiên, lại nhá.
<time>15:28 - 15:37</time> When Mr. Kiên, my direct manager Rabylo announce that I was selected to work in France.
<time>15:37 - 15:43</time> I was surprised, delighted and a little worry.
<time>15:43 - 15:56</time> Although it would be a great opportunity for me to meet talent engineers and expand my experiences in a developed country, I had to be away from my family for a period of time, many things could happen.
<time>15:59 - 16:00</time> Ok đấy.
<time>16:05 - 16:06</time> 2 1 bắt đầu.
<time>16:07 - 16:12</time> great không phải grit nha.
<time>16:13 - 16:13</time> great.
<time>16:14 - 16:14</time> great.
<time>16:14 - 16:15</time> great, great, great.
<time>16:16 - 16:25</time> Although it would be a great opportunity for me to meet talent engineers and expand, expand, expand, expand cái expan.
<time>16:26 - 16:26</time> expand.
<time>16:27 - 16:38</time> Although it would be a great opportunity for me to meet talent engineer and expand my experiences in developed country, I had
<time>16:38 - 16:39</time> to be away.
<time>16:42 - 16:42</time> Lại lại lại.
<time>16:43 - 16:44</time> When
<time>16:44 - 16:45</time> although.
<time>16:45 - 16:56</time> Although it would be a great opportunity for me to meet talent engineers and expand my experiences in developed country, I have to be away from my family for a period time.
<time>16:57 - 16:57</time> Many things could happen.
<time>17:00 - 17:01</time> 3 2 1 bắt đầu.
<time>17:02 - 17:13</time> It was not easy to make decision at that moment.
<time>17:14 - 17:14</time> Okay.
<time>17:16 - 17:17</time> 2 1 bắt đầu.
<time>17:19 - 17:24</time> It was not easy to make decision at that moment.
<time>17:26 - 17:26</time> 2 1 bắt đầu.
<time>17:28 - 17:34</time> My family and co-worker at Rabylo encourage me to seize the opportunity.
<time>17:37 - 17:39</time> hơi chậm quá.
<time>17:39 - 17:40</time> hơi chầm.
<time>17:40 - 17:45</time> My family and co-workers at Rabylo encourage me to re-seize the opportunity.
<time>17:46 - 17:47</time> the opportunity.
<time>17:48 - 17:49</time> đoạn chia giải.
<time>17:49 - 17:50</time> chia ra dấu chấm.
<time>17:51 - 17:52</time> Ok.
<time>17:52 - 17:56</time> cái đoạn mà it was not easy decision hay là hai mấy ạ?
<time>17:57 - 17:59</time> 3 2 1 bắt đầu.
<time>18:01 - 18:08</time> My family and co-worker at Rabylo encourage me to seize the opportunity.
<time>18:11 - 18:12</time> Ok.
<time>18:13 - 18:14</time> 2 1 bắt đầu.
<time>18:15 - 18:25</time> My husband immediately thấp quá.
<time>18:25 - 18:31</time> My husband immediately supports my business trip because he knew the trip could be a great experiences on my way to open up my dream.
<time>18:32 - 18:32</time> Em cứ bị nhìn vào camera.
<time>18:32 - 18:33</time> Lại nha.
<time>18:34 - 18:43</time> My husband immediately supports my business trip because he knew the trip could be a great experience on my way lại lại lại.
<time>18:44 - 18:45</time> Cái này bị cảm xúc nó bị lên cao ấy.
<time>18:46 - 18:46</time> Lại.
<time>18:47 - 18:49</time> My husband.
<time>18:49 - 18:50</time> great, great, great.
<time>18:50 - 18:51</time> My husband.
<time>18:52 - 19:01</time> My husband immediately supports my business trip because he knew the trip could be a great experiences on my way to open up my dream.
<time>19:04 - 19:05</time> Great.
<time>19:05 - 19:06</time> nói xong cứ cười.
<time>19:07 - 19:08</time> Okay.
<time>19:08 - 19:09</time> bắt đầu.
<time>19:11 - 19:18</time> My husband immediately bị thấp ấy, bị cụt ấy.
<time>19:19 - 19:23</time> Lại.
<time>19:23 - 19:34</time> Hoặc là này, hay là my husband supported me right away.
<time>19:34 - 19:35</time> Tức là right away cũng có nghĩa là the same kiểu Immediately, nếu em phải nhếu lưỡi thì sẽ là my husband supported me immediately because he know the trip, okay.
<time>19:37 - 19:38</time> hơi khó.
<time>19:39 - 19:39</time> Trong quá trình quay vẫn sửa suốt mà.
<time>19:40 - 19:41</time> Cứu chị.
<time>19:43 - 19:48</time> My husband supports me right away.
<time>19:50 - 19:51</time> right away.
<time>19:52 - 20:05</time> My husband supported me right away because he knew the trip could be a great experiences on my way to open up my dream.
<time>20:07 - 20:07</time> Lại nhá.
<time>20:07 - 20:15</time> My husband supports me right away because he knew the trip could be a great.
<time>20:15 - 20:18</time> My husband supported me right away.
<time>20:18 - 20:20</time> sau khi nói nhiều á, nó bắt đầu bị rung giọng ở thanh quản.
<time>20:20 - 20:21</time> Hình như thế.
<time>20:22 - 20:22</time> Em lại.
<time>20:23 - 20:26</time> nó sẽ chắc hơn.
<time>20:26 - 20:27</time> Ok.
<time>20:27 - 20:29</time> Em bắt đầu bị lên cao ấy, bắt đầu nói với.
<time>20:29 - 20:34</time> My husband supports me right away.
<time>20:34 - 20:35</time> Đấy, thoát rồi đúng không?
<time>20:36 - 20:36</time> Lại.
<time>20:38 - 20:47</time> My husband supports me right away because he knew the trip could be a great experiences on my way to open up my dream.
<time>20:49 - 20:49</time> Ok.
<time>20:50 - 20:52</time> Ok đấy.
<time>20:53 - 20:54</time> 2 1 bắt đầu.
<time>20:55 - 21:06</time> My husband supports me right away because he knew the trip could be a great experiences on my way to open up my dream.
<time>21:07 - 21:07</time> Ok.
<time>21:08 - 21:09</time> Ok.
<time>21:10 - 21:11</time> 2 1 bắt đầu.
<time>21:13 - 21:18</time> There are two important things I need to prepare.
<time>21:18 - 21:24</time> English and a personal computer equipped with proper security.
<time>21:29 - 21:29</time> Every weekend.
<time>21:32 - 21:33</time> 3 2 1 bắt"""

# --- Tên file CSV đầu ra ---
output_file = "en_dialogue.csv"

# --- Chạy hàm chuyển đổi ---
convert_dialogue_to_csv(dialogue_text, output_file)
