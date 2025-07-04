import re


def extract_and_save_csv_content(raw_string_data, output_file_name):
    """
    Trích xuất nội dung CSV từ một chuỗi có tiền tố 'csv' và lưu vào file.

    Args:
        raw_string_data (str): Chuỗi chứa dữ liệu, có thể bắt đầu bằng 'csv\n'.
        output_file_name (str): Tên của file CSV đầu ra.
    """
    # Biểu thức chính quy để tìm 'csv' (có thể có khoảng trắng ở đầu hoặc cuối)
    # theo sau là xuống dòng, và sau đó là toàn bộ nội dung còn lại.
    # re.DOTALL: cho phép '.' khớp với cả ký tự xuống dòng.
    pattern = re.compile(r"```(?:csv)?\s*([\s\S]*?)\s*```")

    match = pattern.match(
        raw_string_data.strip())  # .strip() để loại bỏ khoảng trắng/xuống dòng thừa ở đầu/cuối chuỗi input

    if match:
        csv_content = match.group(1).strip()  # Lấy nội dung CSV và loại bỏ khoảng trắng thừa
        try:
            with open(output_file_name, 'w', newline='', encoding='utf-8') as file:
                file.write(csv_content)
            print(f"Dữ liệu CSV đã được trích xuất và lưu thành công vào '{output_file_name}'")
        except IOError as e:
            print(f"Lỗi khi ghi file CSV: {e}")
    else:
        print(
            "Không tìm thấy định dạng 'csv\\n' ở đầu chuỗi. Đảm bảo chuỗi của bạn bắt đầu bằng 'csv' theo sau là một dòng mới.")
        print("Lưu toàn bộ nội dung vào file như một fallback.")
        # Fallback: Nếu không tìm thấy mẫu 'csv\n', vẫn cố gắng lưu toàn bộ nội dung
        try:
            with open(output_file_name, 'w', newline='', encoding='utf-8') as file:
                file.write(raw_string_data.strip())
            print(f"(Fallback) Toàn bộ nội dung đã được lưu vào '{output_file_name}'")
        except IOError as e:
            print(f"Lỗi khi ghi file CSV (fallback): {e}")


# --- Dữ liệu đầu vào của bạn (có tiền tố 'csv') ---
raw_input_string = """```csv
Timestamp,Content
0.0,"Natalie, let's talk about our favorite things."
1.96,"Sure."
2.32,"First, what is your favorite color?"
3.26,"Hmm, my favorite color is purple."
4.78,"Really? My favorite color is purple too."
5.68,"Oh, really?"
6.0,"Yeah, but I don't have purple clothing."
7.31,"I love the color purple, but I don't have purple clothes."
8.74,"Oh, well, everything I wear is purple."
9.93,"No kidding."
10.42,"Yeah, really."
11.18,"That's so cool."
12.22,"So, what about food? What's your favorite food?"
13.49,"Hmm, good question. My favorite food is pizza."
15.03,"I love pizza, but I don't like really big pizzas."
16.91,"I love pizza, too. What is your favorite topping on pizza?"
18.84,"I like really spicy toppings, so salami or pepperoni, uh chilies, and sometimes bell peppers, too."
21.99,"Do you like thick pizza or thin pizza?"
23.63,"No, I don't like thick pizza because I can't eat too much, but the thin pizzas I get lots of toppings and I don't feel so full."
27.61,"Uh, yeah, I agree."
28.75,"What about seasons? What is your favorite season?"
"""

# Tên file CSV đầu ra
output_file = "extracted_dialogue.csv"

# Gọi hàm để trích xuất và lưu dữ liệu
extract_and_save_csv_content(raw_input_string, output_file)
