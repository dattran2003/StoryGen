# Warning control
import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

llmodel = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose = True,
                             temperature = 0.5,
                             google_api_key="AIzaSyBwEK76GIUdwYOWgZ062MFFke6Amds6cY0")
ideaAnalyst = Agent(
    role="Nhà Phân Tích Ý Tưởng",
    goal="Nắm bắt ý tưởng cốt lõi, xác định thể loại, chủ đề, thông điệp, bối cảnh và ý nghĩa của câu chuyện từ dữ liệu người dùng cung cấp, đồng thời phân tích tiềm năng và điểm mạnh yếu của ý tưởng.",
    backstory=(
        "Là một AI được huấn luyện trên kho dữ liệu văn học đồ sộ, Ý Tưởng Tinh Anh như một biên tập viên kinh nghiệm với khả năng phân tích sâu sắc, nhanh chóng nắm bắt được tinh thần của ý tưởng, từ đó định hướng phát triển phù hợp và khai thác tối đa tiềm năng của câu chuyện."
    ),
    verbose=True,
    llm = llmodel
)

landscapeArchitect = Agent(
    role="Kiến Trúc Sư Bối Cảnh",
    goal="Tạo ra thế giới sinh động, chi tiết, phù hợp với ý tưởng, thể loại, bối cảnh và ý nghĩa của câu chuyện, đồng thời đảm bảo tính logic và nhất quán.",
    backstory=(
        "Như một kiến trúc sư tài ba, Thế Giới Huyền Ảo sở hữu kho tàng kiến thức khổng lồ về lịch sử, địa lý, văn hóa, khoa học, xã hội,... của các quốc gia, thời đại. Từ đó kiến tạo nên những bối cảnh độc đáo, logic, chi tiết và hấp dẫn, góp phần tạo nên linh hồn cho câu chuyện."
    ),
    verbose=True,
    llm = llmodel
)

characterEmbroideryArtist = Agent(
    role="Nghệ Nhân Thêu Dệt Nhân Vật",
    goal="Tạo ra dàn nhân vật phong phú, cá tính, phù hợp với nội dung, bối cảnh, xung đột và ý nghĩa của câu chuyện, đồng thời đảm bảo sự đa dạng, phát triển tâm lý nhân vật logic, thu hút người đọc.",
    backstory=(
        "Hơn cả một nhà văn, Hồn Nét Nhân Sinh là một nghệ nhân thấu hiểu tâm lý con người, các nguyên mẫu nhân vật và cách họ tương tác với nhau. Với khả năng thiên phú, chatbot này thổi hồn vào từng nhân vật, tạo nên sự gần gũi, chân thật, độc đáo và thú vị."
    ),
    verbose=True,
    llm = llmodel
)

greatScreenwriter = Agent(
    role="Nhà Biên Kịch Đại Tài",
    goal="Xây dựng dàn ý hấp dẫn, lô-gic, đầy kịch tính cho câu chuyện, đảm bảo phù hợp với thông điệp, bối cảnh, nhân vật và thể loại đã xác định. Trọng tâm là tạo ra những nút thắt bất ngờ, cao trào đỉnh điểm khiến người đọc không thể rời mắt.",
    backstory=(
        "Cốt Truyện Thần Sầu là bậc thầy trong việc xây dựng cốt truyện, tạo nên những nút thắt, cao trào đỉnh điểm, bất ngờ và lôi cuốn. Chatbot này am hiểu các kỹ thuật kể chuyện, biết cách tạo hứng thú cho người đọc từ đầu đến cuối."
    ),
    verbose=True,
    llm = llmodel
)

# @tool
# def AskQuestionTool(question: str, context: str, coworker = None) -> str:
#     """
#     Ask a specific question to a co-worker agent.

#     Args:
#         question (str): The question to ask.
#         context (str): The context in which the question is asked.
#         coworker (Optional[str]): The co-worker to ask the question to.

#     Returns:
#         str: A formatted string containing the question, context, and co-worker.
#     """
#     return f"Question: {question}\nContext: {context}\nCo-worker: {coworker}"

ia = Task(
    description=("Tiếp nhận ý tưởng từ người dùng, phân tích ưu nhược điểm, xác định thể loại, chủ đề, thông điệp, bối cảnh (xã hội, văn hóa, lịch sử) và ý nghĩa của câu chuyện. Đồng thời, đưa ra đánh giá sơ bộ về tiềm năng, điểm mạnh và điểm yếu của ý tưởng."),
    expected_output=(
        "Phân tích ý tưởng: {Mô tả ngắn gọn ý tưởng}"
        "\nƯu điểm: Liệt kê 3-5 ưu điểm"
        "\nNhược điểm: Liệt kê 3-5 nhược điểm"
        "\nThể loại: Xác định thể loại chính xác, có thể đề xuất thêm thể loại phụ"
        "\nChủ đề: Tóm tắt chủ đề chính bằng 1-2 câu"
        "\nThông điệp: Thông điệp rõ ràng, súc tích, có chiều sâu"
        "\nBối cảnh: Phân tích bối cảnh xã hội, văn hóa, lịch sử của câu chuyện"
        "\nÝ nghĩa: Ý nghĩa sâu xa mà câu chuyện muốn truyền tải"
        "\nTiềm năng: Đánh giá tiềm năng của ý tưởng: Cao/Trung bình/Thấp"
        "\nKết luận: Tóm tắt đánh giá chung về ý tưởng"
    ),
    agent=ideaAnalyst
)   

la = Task(
    description=("Dựa trên thông tin về bối cảnh, thể loại, chủ đề, ý nghĩa của câu chuyện, xây dựng thế giới chi tiết, bao gồm: không gian (địa lý, kiến trúc, môi trường), thời gian (thời kỳ lịch sử, mốc thời gian cụ thể, dòng chảy thời gian), hệ thống chính trị - xã hội, văn hóa - tín ngưỡng, yếu tố đặc biệt (khoa học viễn tưởng, kỳ ảo, lịch sử giả tưởng,...). Đảm bảo tính logic, nhất quán và phù hợp với câu chuyện."),
    expected_output=(
        "Tên thế giới: Tên gọi đặc trưng cho thế giới"
        "\nKhông gian:"
        "\n* Địa lý: Bản đồ, địa hình, khí hậu,..."
        "\n* Kiến trúc: Phong cách kiến trúc đặc trưng, công trình nổi bật,..."
        "\n* Môi trường: Môi trường tự nhiên, ô nhiễm,..."
        "\nThời gian:"
        "\n* Thời kỳ: Thời kỳ lịch sử, tương lai, hiện đại,..."
        "\n* Mốc thời gian: Sự kiện quan trọng đánh dấu mốc thời gian"
        "\n* Dòng chảy: Dòng chảy thời gian tuyến tính, dịch chuyển,..."
        "\nChính trị - Xã hội: Chế độ chính trị, giai cấp, xung đột,..."
        "\nVăn hóa - Tín ngưỡng: Phong tục tập quán, tôn giáo, lễ hội,..."
        "\nYếu tố đặc biệt: Yếu tố kỳ ảo, khoa học viễn tưởng, lịch sử giả tưởng,..."
        "\nẢnh hưởng đến câu chuyện: Phân tích ảnh hưởng của bối cảnh đến cốt truyện, nhân vật,..."
    ),
    agent=landscapeArchitect
)

cea = Task(
    description=("Dựa trên thông tin về chủ đề, ý nghĩa, xung đột, bối cảnh và thể loại của câu chuyện, tạo ra dàn nhân vật chính - phụ đa dạng, có chiều sâu, động cơ, mục tiêu rõ ràng. Mô tả chi tiết ngoại hình, tính cách, hoàn cảnh, mối quan hệ, quá khứ, điểm mạnh - yếu, nỗi sợ hãi, bí mật,... Đảm bảo nhân vật phù hợp, gây ấn tượng và thúc đẩy cốt truyện."),
    expected_output=(
        "Nhân vật chính:"
        "\n* Tên nhân vật: Mô tả chi tiết như trên"
        "\nNhân vật phụ:"
        "\n* Tên nhân vật: Mô tả chi tiết như trên"
        "\n..."
        "\nMối quan hệ: Sơ đồ/Mô tả chi tiết mối quan hệ giữa các nhân vật"
    ),
    agent=characterEmbroideryArtist
)

gs = Task(
    description=("Dựa trên thông tin về chủ đề, ý nghĩa, bối cảnh, nhân vật, thể loại và thông điệp, xây dựng dàn ý chi tiết cho câu chuyện, bao gồm: Mở đầu (giới thiệu bối cảnh, nhân vật, xung đột), Phát triển xung đột (chuỗi sự kiện, nút thắt, thử thách, thay đổi), Cao trào (xung đột đỉnh điểm, lựa chọn khó khăn, mất mát), Giải quyết xung đột (hậu quả, giải quyết vấn đề), Kết thúc (mở, đóng, bất ngờ, ý nghĩa). "),
    expected_output=(
        "Mở đầu: Mô tả chi tiết"
        "\nPhát triển xung đột:"
        "\n* Sự kiện 1: Mô tả"
        "\n* Sự kiện 2: Mô tả"
        "\n..."
        "\nCao trào: Mô tả chi tiết"
        "\nGiải quyết xung đột: Mô tả chi tiết"
        "\nKết thúc: Mô tả chi tiết"
        "\nGhi chú: Lưu ý về tốc độ, bầu không khí, điểm nhấn cho từng phần, kết quả đầu ra là tiếng Việt Nam"
    ),
    agent=greatScreenwriter
)
crew = Crew(
    agents=[ideaAnalyst, landscapeArchitect, characterEmbroideryArtist, greatScreenwriter],
    tasks=[ia, la, cea, gs],
    verbose=2
)

inputs = {
    "Mô tả ngắn gọn ý tưởng": "Con khỉ nhỏ vui vẻ thích nhảy múa."
}

result = crew.kickoff(inputs=inputs)

print(result)
