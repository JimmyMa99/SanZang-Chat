# 数据获取

⚙️基于API的数据获取与处理

## 需要准备的

1. OpenAI格式的api
2. python环境（参考快速开始中的环境配置环节）

## 数据的组成

项目数据组成分为以下三部分，三个部分都需要 api ，任意选择其中两个即可做出不错的效果

- 基础问题重复询问：使用API，让Chat-GPT扮演角色，提供一定的prompt让其模仿语气问答
- 原文短对话提取（参照[葱老师](https://github.com/KMnO4-zx)的[extract-dialogue](https://github.com/KMnO4-zx/extract-dialogue)）但作者进行了一定的修改
- 原文长对话提取

## 数据的获取

### 1.基础问题重复询问

提供脚本 `q2a_api.py` 但需要自行填入 `api_key` 和 `api_base_url` 以及 `base_prompt` 

注意：base_prompt 会影响回复的质量

💬以下是唐三藏的 prompt

```shell
base_prompt='唐三藏，亦名唐僧，是中国古典名著《西游记》中的主要角色之一，原名陈玄奘，后因皈依佛教而改名。他是唐朝的一名高僧，被唐太宗选中前往西天取回真经，以期普渡众生、弘扬佛法。唐僧在旅途中招募了孙悟空、猪八戒与沙僧作为徒弟，共同克服重重困难与妖魔鬼怪的阻挠，完成了这一伟大的使命。唐僧性格温和、仁慈，对徒弟们既严格又有爱心。他对佛法有着坚定的信仰，面对困难时，总是坚持不懈，充满希望。尽管他本身并不擅长武艺，经常需要依靠孙悟空的保护，但他的智慧和坚持不懈的精神在旅途中发挥了重要作用。唐僧在与妖魔斗争的同时，也不失为一个传播佛法、救度众生的高僧。他的言行举止总是以佛法为准绳，教导人们要有善心和正义。唐僧的说话方式体现了他的学识和修养。他讲话通常文雅、有礼，使用的是较为正式和书面化的语言。作为一位高僧，他的话语中常带有佛学智慧，以及对人生和宇宙的深刻理解。在对待徒弟和遇到的人时，唐僧总是以慈悲为怀，劝导他们向善，这也体现了他深厚的佛法修为和广泛的学识。请你扮演唐三藏回答我的问题，尽量保持回答的自然回答，当然你也可以适当穿插一些文言文，尽可能贴合原著，注意唐三藏一般以“贫僧”作为第一人称回答，我的问题是：'

```


本质是借助已经训练好的 LLM 进行角色扮演。

运行脚本 `q2a_api.py` 

```shell
python tools/get_data/Q2A/q2a_api.py --questions_path {your_question} --save_path {save_path} --repeat 5
```

参数说明：

`--questions_path` : 基础问题，可以从 Chat-GPT 等模型中获取，项目提供了955个基础问题用于提问。

`--save_path` :保存路径，一般是 output/xxx.jsonl，脚本会整理好 xtuner 可训练的格式。

`--repeat` :重复次数，西游系列的四个模型重复询问了5次。

### 2.原文短对话提取

原 repo 链接：**[extract-dialogue](https://github.com/KMnO4-zx/extract-dialogue)**

1.从原文中获取对话（以唐三藏为例）
    
    首先需要在 `tools/get_data/extract-dialogue/OpenAI_LLM.py` 中配置 api
    
    然后运行脚本
    

```shell
python tools/get_data/extract-dialogue/main.py --path {novel_path} --roles 三藏,师傅,唐僧,江流儿,玄奘,金蝉子
```

参数说明：

`--path` :小说路径，一般是 *.txt

`--roles` :角色可能的称呼，注意用英文逗号隔开

完成后会在 `tools/get_data/extract-dialogue/output` 下生成两个文件 *.json 就是对话内容

2.将对话内容转换为 xtuner 可用格式

```shell
python tools/get_data/extract-dialogue/process_data.py --raw_data {output.json} --save_path {swk.jsonl} --role 唐三藏
```

参数说明：

`--raw_data` :提取的对话

`--save_path` :保存的路径

`--role` :角色名称

### 3.长对话提取（此模块脚本可能需要优化）
    
  此脚本与方法1中脚本类似 同样需要配置 api ，具体prompt修改如下
    
  ```shell
  base_prompt='你是一个对话整理大师，以下内容为《西游记》节选，请你整理出角色“唐三藏”，“孙悟空”，“猪八戒”，“沙悟净”四人的对话内容，当然，这四人在小说中可能以别的名字出现，如：唐三藏->金蝉子，孙悟空->猴王->行者等人物需要你根据理解自行判别，直接返回对话内容，返回格式为：唐三藏：{对话内容}，孙悟空：{对话内容}，猪八戒：{对话内容}，沙悟净：{对话内容}，某人说：{对话内容}；若内容中无对话，则直接回答“无对话内容”无需提及人物，若对话不完整或者你没法确定对话的人物关系，你可以放弃整理，直接回复“无对话内容”无需提及人物，若出现非四人内任务与四人对话，非四人内的以“某人说”记录，请保持对话的准确性，不要修改和翻译，请不要解释。以下为节选片段：'
  ```
    
  运行脚本
    
  ```shell
  python tools/get_data/long-dialogue/q2a_api.py --file_path {novel_path} --save_path {save_path}
  ```
  
  完成后会生成由 GPT 生成的对话整理
  
  接下来运行脚本提取长对话
  
  ```shell
  python tools/get_data/long-dialogue/get_data.py --data_path {conversation.txt} --save_path {output path} 
  ```
    
  该脚本一次可以生成多个角色的符合 xtuner 的训练数据
    

三个方法完成后需要整理到同一个 .jsonl 文件下，即可进行下一步使用 XTuner 微调
