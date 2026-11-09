# Llama 固定模型卡公开网页读取记录

读取日期：2026-11-07 UTC。
来源：https://huggingface.co/meta-llama/Llama-3.1-8B/blob/d04e592bb4f6aa9cfee91e2e20afa771667e1d4b/README.md
读取方式：网页检索工具直接打开上述固定提交页面。页面标题和提交标识均为 d04e592。此文件为核验记录，不冒充网页原始存档。

页面模型信息写明 8B、公开在线数据新混合、15T+ tokens、2023-12 知识截止，并称模型为离线训练的静态模型。使用部分提供 Transformers 4.43.0 起的示例及原始 llama 仓库入口。训练设施部分说明采用 Meta 自定义训练库和生产基础设施。许可部分指向 Llama 3.1 Community License，包含归属、用途政策和特定规模的额外授权条件；模型卡用途说明也允许在遵守许可条件下用输出改进其他模型，包括合成数据和蒸馏。

公开 revision API 的 SHA、文件清单和 cardData 另存为 meta-llama--Llama-3.1-8B--revision-api.json。随后受控原始文件读取返回 401，未再尝试获取该受控原始文件，未登录或接受许可。可读公开网页内容与受控下载能力分别记录。
