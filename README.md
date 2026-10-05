# todo-agent-lite

零依赖的「自然语言 → 待办管理」CLI。规则解析中文一句话（明天/下周一+事项），增删改查/列出待办，状态存 JSON。

## 快速开始

```bash
python -m todo_agent_lite "明天下午三点开会"
python -m todo_agent_lite "列出待办"
python -m todo_agent_lite "把 1 标记为完成"
python -m todo_agent_lite
```

## 无 API Key 如何运行

纯规则解析，不调用任何 LLM，不需要任何 API Key。

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## License

MIT © ljiang9
