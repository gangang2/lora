本教程是利用llmware实现全自动数据数据提取制作微调数据集+lora微调llama3

将PDF、PPT、DOCX这些格式不统一的文档制作成统一可用于大模型微调的训练数据是一件麻烦的事情

其中涵盖了将文件中的文字、表格、图标分别提取 并再各自提取文本

现在可以利用LLmWare框架(https://github.com/llmware-ai/llmware/)
llmware包含了多个小型且经过微调的专业模型，囊括了分类，总结、提取等功能
其中，library模块负责大规模摄取、组织和索引知识集合——解析、文本块和嵌入。

这里我们将利用它来负责将现有的各种各样的文档制作成数据集

使用教程:

需要在linux环境执行 windows系统安装wsl和ubuntu后，在启动wsl，在linux环境下安装conda

执行
pip install llmware

接下来执行
python slicing_and_dicing_office_docs.py


执行代码文件：
![image](https://github.com/user-attachments/assets/0fa97855-3015-49cd-8b39-005507d9e5bf)

library会解析所有文件 并分类 文字、表格、图片
一旦内容被分类，就需要使用相应的工具和方法来处理它们：

文本内容：直接提取和使用。

表格内容：专门的表格解析工具来提取数据。

图像内容：使用OCR技术来从图像中提取文本

最终我们会将他们汇聚成训练集jsonl
![image](https://github.com/user-attachments/assets/7b322f4f-20cf-4645-a5ed-c3fb3e7a188b)


之后将数据集拿来训练llama3
https://colab.research.google.com/drive/1dhYeH4-saJ7urqpisCfm-2ZCRIkiOCAH?usp=sharing
可以发现llama3训练好可以回答有关微软2024第四季度财报的相关内容了，因为我们的数据集就是扒的微软的报告会议记录
![1724593113618](https://github.com/user-attachments/assets/83e45b85-753e-412a-8d6e-6ae3d304016d)






