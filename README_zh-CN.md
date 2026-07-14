# 具有预先规定泄漏控制与化合物谱相似性诊断的留出 herb 靶标优先排序基准

**作者：** Chenyu Hu，Xinyou Zhang

**单位：** 江西中医药大学智能医学与信息工程学院，江西南昌 330004，中国

**通讯作者：** Xinyou Zhang（xinyouzhang@jxutcm.edu.cn）

## 中文摘要

**背景：** herb-target 图模型的可靠评价容易受实体重叠、共享图上下文、不完整正例标签和测试后适应的影响。我们建立了一个带有预先规定泄漏控制的留出 herb 靶标优先排序基准。该控制包括分区间精确规范化名称阻断、对留出 herb-target 标签和 query 特异身份特征的访问限制、基于验证集的模型选择和对测试后适应的限制。该定义不意味着分区在相似性上完全不重叠，也不意味着与上游来源构建完全独立。

**结果：** 在历史 sealed test 中，HeteroSAGE 的平均 herb-level macro AUPR 最高（0.682663，样本 SD 0.010937），TCMRGAT（0.679919，SD 0.005636）和 GCN（0.679086，SD 0.007807）非常接近。三者均值差小于 0.004，且最佳模型随 seed 改变，因此仅作描述性解释。仅在验证集上进行的诊断提示，化合物谱最近邻迁移是强启发式比较器。

**结论：** 本基准将冻结评价协议、聚合复现材料和诊断结合起来，用于区分模型家族比较与化合物谱相似性及已记录标签覆盖度的影响。结论适用于预先规定的信息边界，而不外推为相似性不重叠、来源完全独立或临床泛化。

## v1.2 开放复现包说明

本目录是“held-out-herb target-prioritization benchmark”的 v1.2 开放复现发布包。论文标题、作者和摘要见 README.md；本中文说明以可复现性与可上传性为重点。

## v1.2 与 v1.1 的关键区别

历史上的一次性 sealed test 被保留为结果来源记录，但本包已经公开固定测试集。因此，包内提供：

- 67 个测试 herb；
- 8,632 个 recorded-positive herb-target pairs；
- 2,309 个候选 target 的固定顺序；
- 冻结图输入和测试 herb 的 query context；
- 5 个模型、每个 5 个 seed 的 25 个 best checkpoint；
- 25 个完整的 raw decoder-logit 分数矩阵；
- 可独立运行的第三方分数矩阵评价程序。

公开后，这一测试集不再是盲测或持续保密的 held-out test。不得用它进行超参数调优、模型选择、checkpoint 选择、特征设计或测试后方法开发。历史 sealed-test 结果与公开后的冻结复现结果必须区分表述。

## 如何独立评价

已有包内模型分数时，可运行：

    python src/evaluation/evaluate_score_matrix_v1.py ^
      --package-root . ^
      --score-matrix artifacts/scores/TCMRGAT__CFG04__FINAL_01_scores_v1.npz ^
      --output audits/generic_evaluator_smoke_TCMRGAT__CFG04__FINAL_01.json

第三方模型可提供一个 NPZ 文件，其中必须同时含有：

    scores: 形状为 (67, 2309) 的 float32 或 float64 矩阵
    herb_ids: 与公开测试集完全一致且顺序完全一致的 67 个 ID
    target_ids: 与候选 target 列表完全一致且顺序完全一致的 2,309 个 ID

评价器会拒绝轴缺失、重复、替换或顺序不同的文件，不会静默重排。评分使用的是 archived recorded-positive labels，因此结果表示对已记录正例的检索能力，并不等同于未标注关系在生物学上为阴性。

## 如何复现冻结模型分数

在合适的 Python/PyTorch 环境中运行：

    python src/evaluation/export_frozen_test_scores_v1.py ^
      --package-root . ^
      --device cuda:0 ^
      --query-batch-size 16 ^
      --verify-atol 1e-6 ^
      --verify-rtol 1e-6

该命令不会训练、调参或重新选择模型。它会验证 25 个固定 checkpoint、冻结代码哈希、67 个 herb、2,309 个 target 和 8,632 个正例，并将复现指标与历史 sealed-evaluation 参考结果逐项比较。当前草稿中已完成该检查：275 个 checkpoint-metric 比较全部在 1e-6 的绝对和相对容差内匹配。

## 许可与来源边界

代码目录 src 和 scripts 按 MIT License 使用。图、测试标签、冻结图、权重、分数和结果没有被简单地冠以一个覆盖全仓库的许可证；它们的复用需同时遵守 Dryad、ChEMBL、HGNC、UniProt 和 STRING 等来源的条款。请先阅读 DATA_LICENSE.md、data/licenses/SOURCE_LICENSES.md 和 data_availability/source_provenance_license_matrix.csv。

本包公开的是可执行的冻结派生快照，不是所有第三方原始数据库记录的镜像。尤其是，历史 ChEMBL 提取版本和所有 target-target 筛选细节不能完全从现有归档中恢复；详见 data/provenance/UPSTREAM_VERSION_LIMITATION.md。

为保护隐私，复制 checkpoint 元数据中的本机绝对路径已替换为可移植的 historical_provenance 标识符。该操作改变了 checkpoint 文件的序列化 SHA-256，但不改变 state_dict 张量内容；历史与发布版哈希以及 state_dict 指纹见 data/provenance/checkpoint_metadata_path_sanitization_v1.json。

## 归档状态

本版本的 Zenodo version-specific DOI 为 https://doi.org/10.5281/zenodo.21352219。v1.1 归档保持不变；在论文中提及公开测试标签或分数矩阵时，应引用本 v1.2 版本而不是 v1.1。完整发布核对清单见 release_notes/UPLOAD_CHECKLIST_v1.2.md。
