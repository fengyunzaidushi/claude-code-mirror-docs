![cover_image](https://mmbiz.qpic.cn/mmbiz_jpg/7RcnJwSoAPVxagZWSJPeswqHslLupyU8QSHqVJ3cicPqOiapO6csszN3cWibjbHySWA0yYRzrlwmGVUdmhTvnuCBQ/0?wx_fmt=jpeg)

#  AI编程的“监工”秘籍：Claude遇瓶颈时，如何让它连续干活8小时不爆上下文？

Jingmofintech  [ 京墨AI研习社 ](javascript:void\(0\);)

__ _ _ _ _

#  

大家好，我是京墨，专注AI工具与编程实践。今天，我想和大家聊聊一个让我又爱又恨的AI编程助手——Claude。Claude在代码生成和调试上超级强大，但一遇到大项目，数据量稍多、架构稍复杂，就容易“翻车”。我自己就深有体会：项目数据堆积如山，debug时层层嵌套的逻辑一展开，Claude的上下文就爆了；或者用量直接超限，只能干瞪眼等着重置。那种“明明思路清晰，却被技术限制卡住”的挫败感，简直不爽到爆！

不过，好消息是，最近在社交平台上看到一个高赞帖子，分享了一个巧妙的“监工”方案，让Codex（OpenAI的代码代理）连续工作8小时，上下文稳如老狗。
这个思路太有借鉴意义了！基于我的亲身经历，我结合这个方案，整理出一篇实用指南。希望能帮到那些像我一样“被Claude卡住”的开发者。走起！

##  痛点直击：Claude在复杂项目中的“隐形杀手”

先说说我的故事吧。上周，我在用Claude
Code调试一个中型Web应用：涉及海量JSON数据处理、异步API调用和多层组件架构。一开始，一切顺风顺水——Claude帮我快速生成
boilerplate 代码，调试时还能一步步分析栈溢出。但项目推进到中段，数据量飙升到GB级，debug日志像雪崩一样涌来。结果呢？

  * ** 上下文爆掉  ** ：Claude会智能地自己总结（summary）之前的对话，继续响应我的指令。这点还算人性化，至少没彻底中断。 
  * ** 用量爆掉  ** ：更要命的是token用量超限！Claude直接“罢工”，提示我等待重置期（通常几小时）。我只能暂停工作，喝杯咖啡发呆，效率直线坠落。 

这种体验，让我感觉AI编程像“半成品”——潜力无限，却总在关键时刻掉链子。数据量大、架构复杂是常态，尤其在企业级开发中，谁没遇过？如果你也这样，恭喜，你不是一个人在战斗。

##  灵感来源：大神宝玉的“Claude监工”方案

刷时，我偶然看到@dotey（宝玉）的帖子：他竟然让Code连续工作8小时，上下文零溢出！ 核心思路是：用Claude
Code当“监工”，监督Code“工人”分步干活。为什么这么牛？因为它巧妙避开了AI的两大痛点——上下文积累和用量限制。

宝玉的方案步骤超清晰，我直接复盘一下（结合他的提示词和截图）：

![](https://mmbiz.qpic.cn/mmbiz_png/7RcnJwSoAPVxagZWSJPeswqHslLupyU8xgEQbiazjpKtZsZMPO2qqAR0Vuib1Q7ickOnVLiciaA04mJDomwJ2v2mtoQ/640?wx_fmt=png&from=appmsg)

1\.  ** 准备TODO List：让工人知道“下一步干啥”  **

  * 先让Code生成一个任务清单（TODO List），细化到可一步步完成的粒度。比如，调试Web app时：TODO1=“解析JSON数据”；TODO2=“优化异步调用”；TODO3=“测试边缘case”。 
  * 更新Agents.md文件，添加规则：如果输入“continue”，就读取TODO文件，挑选下一个任务，执行后更新TODO。 
  * 这样，每次启动Code都像“接力棒”，不用从头回忆整个项目历史。 

###  2\.  ** Claude Code启动&监控：用命令行一键驱动  **

  * Claude Code执行命令：  ` eport TERM=term && code eec "continue to net task" --full-auto  ` 。 
  * 这会启动一个全新的Code session，传入固定提示“continue to net task”。由于是新会话，上下文从零开始，不会积累爆掉。 
  * 监工模式：Claude Code实时观察Code执行。如果任务完成（宝玉建议多等会儿，避免假阳性），就杀掉进程，重新启动下一个。 

###  3\.  ** 防上下文爆的杀手锏：子Agent独立作战  **

  * 关键在这里！Claude Code每次启动/监控Code时，都开一个  ** 子Agent  ** （用Task Tool实现）。每个子Agent有独立上下文，主Agent只接收最终结果，占用空间小到忽略不计。 
  * 宝玉的提示词示例： 

> 帮我在当前目录下，新开一个agent，使用 eport TERM=term && code eec "continue to net task"
> --full-auto 命令开启一个 code 进程,
> 注意观察任务执行情况，如果当前任务完成(任务运行时间较长，可以多等一会)，就结束进程，然后重新开个agent运行相同指令让它继续。注意每次打开code和监控它运行都调用一个新agent
> (Task Tool)来执行这个操作以避免主agent上下文太长。

运行效果？宝玉的截图显示：Code稳稳推进，8小时无中断！ 当然，他也吐槽Claude Code偶尔“偷懒”中断，但整体思路稳。

![](https://mmbiz.qpic.cn/mmbiz_jpg/7RcnJwSoAPVxagZWSJPeswqHslLupyU8ARAssukP6d7iaWERFFWhgzAwVy50ID33nRSXQKhyIPRoccYqibNicjvhA/640?wx_fmt=jpeg&from=appmsg)

##  如何应用到我的Claude痛点？个性化改造指南

宝玉的方案针对Code，但我直接“移植”到Claude Code上，效果拔群！因为Claude Code本身支持Task
Tool和子进程，天然适合“监工”角色。结合我的大项目经历，改造如下：

  * ** 针对数据量大  ** ：TODO List拆分数据处理任务，比如“先处理前10%数据，验证后继续”。子Agent监控输出文件，避免日志洪水淹没上下文。 
  * ** 针对复杂debug  ** ：在Agents.md中加debug规则——每个任务输出独立日志文件，主Claude只看summary。遇到用量超限？用子Agent轮换，相当于“换班休息”。 
  * ** 我的实践  ** ：上周重试那个Web app，用这个方案，Claude连续跑了4小时（用量没爆），debug效率翻倍。唯一小坑：Claude有时“自作主张”中断，我加了定时检查脚本补救。 

变体玩法（从回复中get灵感）：

  * ** Python脚本自动化  ** ：像@jesselaunz分享的，用脚本监控完成文件，n秒后自动close&重启Claude。 适合不爱命令行的朋友。 
  * ** Warp终端编排  ** ：@zhangjintao9020建议用Warp作为“超级监工”，无用量限，还能压缩上下文。 终端党必试！ 
  * ** Hook机制  ** ：Claude Code支持hook，结合脚本实现全自动化循环。 

##  结语：AI编程，从“卡顿”到“流畅”，就差一个思路

Claude的上下文和用量限制，是当前AI工具的“成长痛”，但像宝玉这样的方案，证明了：我们可以用工程思维绕过去。记住，核心是  ** 模块化+独立上下文
** ——让AI像流水线工人，分步协作。

如果你也正纠结Claude的瓶颈，不妨试试这个“监工”法。欢迎在评论区分享你的改造经验，或吐槽AI的奇葩bug！下期见，我们继续解锁AI黑科技~

（图片来源：帖子截图，感谢@dotey分享灵感）

_ 公众号：京墨金融，更多AI编程干货，关注不迷路！  _

  

预览时标签不可点

[ 阅读原文 ](javascript:;)

微信扫一扫  
关注该公众号



微信扫一扫  
使用小程序

****



****



****



×  分析

__

![作者头像](http://mmbiz.qpic.cn/mmbiz_png/7RcnJwSoAPXicDXDz5Z2sWHdgdXfibFHqib9BrE583ly9vYZKsrMvvIBOOzTKu8dynt7mZFcY6VVWTMSevwgHsbiaA/0?wx_fmt=png)

微信扫一扫可打开此内容，  
使用完整服务

：  ，  ，  ，  ，  ，  ，  ，  ，  ，  ，  ，  ，  。  视频  小程序  赞  ，轻点两下取消赞  在看  ，轻点两下取消在看
分享  留言  收藏  听过

