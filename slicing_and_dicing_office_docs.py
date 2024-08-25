import os
import zipfile
from llmware.library import Library
from llmware.configs import LLMWareConfig
from llmware.setup import Setup
from llmware.retrieval import Query
from llmware.dataset_tools import Datasets

# 这里指定了本地的文件目录
def create_microsoft_ir_library(library_name="microsoft_ir", file_path="./FY24Q4-zip.zip"):
    """ Uses the locally downloaded Microsoft IR sample files - parses, text chunks and creates Library. """
    print("update: using the locally downloaded microsoft investor relations sample files")

    # 解压ZIP文件到临时目录
    temp_dir = "./tmp/microsoft_ir_files"
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    print("update: extracted files to temporary directory: ", temp_dir)

    my_lib = Library().create_new_library(library_name)

    # 解析解压后的文件，添加智能化分块，捕捉标点符号或回车
    parsing_output = my_lib.add_files(temp_dir, chunk_size=400, max_chunk_size=600, smart_chunking=1,
                                      get_tables=True, get_images=True)
# 上面这行代码捕捉文档中的表格和图片，接入ocr或做csv提取
    print("update: parsing output: ", parsing_output)

    # 打印出提取的图片路径
    print("update: images extracted to path: ", my_lib.image_path, my_lib.output_path)

    # 执行一个简单的文本查询
    qr = Query(my_lib).text_query("azure", result_count=10)

    for i, res in enumerate(qr):
        print("results: ", i, res)

    return my_lib  # 返回Library实例以便进一步使用，这里用到了一个小模型，完成测试

def slice_and_dice_special(lib_instance):
    # 加载已经创建的lib实例
    lib = lib_instance

    # 导出所有表格数据到CSV
    q = Query(lib)
    extracted_tables = q.export_all_tables(output_fp=lib.output_path)
    print("extracted tables summary: ", extracted_tables)

    # 运行OCR
    lib.run_ocr_on_images(add_to_library=True, chunk_size=400, min_size=10, realtime_progress=True)
    print("done with ocr processing")

    # 导出数据到JSONL文件
    output = lib.export_library_to_jsonl_file(lib.output_path, "microsoft_ir_lib")

    # 创建训练数据集
    ds = Datasets(library=lib, testing_split=0.10, validation_split=0.10, ds_id_mode="random_number")
    ds_output = ds.build_text_ds(min_tokens=100, max_tokens=500)
    print("done with dataset")

    return True

# 主执行脚本
if __name__ == "__main__":
    # 设置活动数据库为SQLite
    LLMWareConfig().set_active_db("sqlite")

    # 定义图书馆名称
    ln = "microsoft_investor_relations"

    # 使用本地文件构建
    my_library = create_microsoft_ir_library(library_name=ln, file_path="./FY24Q4-zip.zip")

    # 运行数据分割和加工，传递Library实例
    slice_and_dice_special(my_library)
