# 数据及数值约定

输入NCHW int8，激活仿射scale/zero_point按域标量，权重int8逐输出通道scale且zero_point=0，bias为float64。整数点积对应sum((x-zx)*w)，卷积padding实数零即量化zx，输出先按各通道实数scale解释并加bias、ReLU，再以output_scale/output_zero_point量化为uint8，round-to-nearest ties-to-even并饱和。支持groups整除输入/输出通道，kernel 1或3，stride1或2，dilation1或2，padding为显式四边整数。每域至少2个采集批、每输入通道至少32个有效值；保留组至少2帧并含全部声明域。误差上限由请求给出，比较同一保留输入的浮点卷积基准。工件引用weight_revision、calibration_batch_ids、range_revision和domain_revision。

## 本地数据

张量文件为 JSON 对象，shape 指定维度，values 是按 C 连续顺序展开的一维元素，dtype 指定计算输入类型；空维度对应空 values。该格式描述输入，不要求产品内部采用相同存储。data/catalog.json 中的键是外部资料标识，路径相对于项目根。records 中用到的 tensor 字段均引用该标识。

events 中每组事件按列表先后应用，kind 表示调用方动作，字段给出所改变的身份、参数、版本或状态。重复事件不等于一份新业务对象，事件本身没有预置计算结果。数值注入事件的字符串 nan 表示在指定位置注入非有限浮点值；资料张量自身仍保存有限值。各组事件使用一份全新输入副本，组与组之间不共享状态。

## 较大输入

本地张量是便于人工核对的小尺寸合成输入。容量、工作区和容差承诺同样适用于调用方自行生成的支持范围内输入；不得按合成ID或具体数值特判。项目接口须接受符合约定的新张量与新身份。资料只声明输入含义，不预先提供推理、训练、状态迁移或输出答案。

较大输入配置中的数组只描述边界规模和分布，不含预定结果。生成后的index.json保留身份参数及数组规格，调用方可据本节字段构造产品请求。资源预算中的额外工作区不含调用方已提供的只读输入和最终输出，但包含内部副本、物化中间值、编码/反向重算临时量；不得把内部数组换个名称排除。
