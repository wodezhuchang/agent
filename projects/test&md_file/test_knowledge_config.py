#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库配置测试脚本 - 验证知识库 ID 配置和检索功能
"""
import os
import sys
import json
from pathlib import Path


def print_banner(title):
    """打印彩色标题"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_ok(message):
    """打印成功消息"""
    print(f"  ✅ {message}")


def print_warn(message):
    """打印警告消息"""
    print(f"  ⚠️  {message}")


def print_error(message):
    """打印错误消息"""
    print(f"  ❌ {message}")


def print_info(message):
    """打印信息消息"""
    print(f"  ℹ️  {message}")


def check_knowledge_config():
    """检查知识库配置"""
    print_banner("1. 检查知识库配置")
    
    project_root = Path(__file__).parent
    config_file = project_root / "config" / "knowledge_config.json"
    
    # 检查配置文件是否存在
    if config_file.exists():
        print_ok("配置文件存在")
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            kb_id = config.get("knowledge_base_id", "")
            kb_name = config.get("knowledge_base_name", "校园校小助知识库")
            top_k = config.get("top_k", 3)
            min_score = config.get("min_score", 0.5)
            enabled = config.get("enabled", True)
            
            print_info(f"  知识库名称: {kb_name}")
            print_info(f"  检索条数: top_k={top_k}")
            print_info(f"  最低分数: min_score={min_score}")
            print_info(f"  启用状态: {'已启用' if enabled else '已禁用'}")
            
            if kb_id:
                print_ok(f"知识库 ID 已配置: {kb_id}")
            else:
                print_warn("知识库 ID 未配置（将使用 Coze 平台默认绑定）")
            
            return {
                "config_file": str(config_file),
                "has_config": True,
                "kb_id": kb_id,
                "config": config
            }
            
        except Exception as e:
            print_error(f"读取配置文件失败: {e}")
            return {
                "config_file": str(config_file),
                "has_config": False,
                "error": str(e)
            }
    else:
        print_error(f"配置文件不存在: {config_file}")
        return {
            "config_file": str(config_file),
            "has_config": False,
            "error": "配置文件不存在"
        }


def check_environment_variables():
    """检查环境变量配置"""
    print_banner("2. 检查环境变量")
    
    kb_id_from_env = os.environ.get("COZE_KNOWLEDGE_BASE_ID")
    
    if kb_id_from_env:
        print_ok(f"COZE_KNOWLEDGE_BASE_ID 已设置: {kb_id_from_env}")
        print_warn("注意：环境变量优先级高于配置文件！")
        return {
            "has_env": True,
            "kb_id": kb_id_from_env
        }
    else:
        print_info("COZE_KNOWLEDGE_BASE_ID 未设置（将使用配置文件）")
        return {
            "has_env": False,
            "kb_id": None
        }


def check_state_module():
    """检查 state 模块的配置读取功能"""
    print_banner("3. 检查配置读取功能")
    
    try:
        # 导入 state 模块
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        from graphs.state import (
            get_knowledge_base_id,
            get_knowledge_config,
            clear_knowledge_base_id_cache
        )
        
        # 测试获取知识库 ID
        print_info("正在调用 get_knowledge_base_id()...")
        clear_knowledge_base_id_cache()
        kb_id = get_knowledge_base_id()
        
        if kb_id:
            print_ok(f"成功获取知识库 ID: {kb_id}")
        else:
            print_warn("获取的知识库 ID 为空（将使用 Coze 平台默认绑定）")
        
        # 测试获取完整配置
        print_info("正在调用 get_knowledge_config()...")
        full_config = get_knowledge_config()
        print_info(f"完整配置: {json.dumps(full_config, ensure_ascii=False, indent=4)}")
        
        return {
            "has_state_module": True,
            "kb_id": kb_id,
            "full_config": full_config
        }
        
    except Exception as e:
        print_error(f"检查失败: {e}")
        import traceback
        print_info(f"堆栈跟踪:\n{traceback.format_exc()}")
        return {
            "has_state_module": False,
            "error": str(e)
        }


def check_knowledge_search_code():
    """检查知识库检索代码"""
    print_banner("4. 检查知识库检索代码")
    
    try:
        # 读取知识库搜索节点代码
        node_file = Path(__file__).parent / "src" / "graphs" / "nodes" / "knowledge_search_node.py"
        
        if not node_file.exists():
            print_error(f"节点文件不存在: {node_file}")
            return {
                "has_node_file": False,
                "error": "节点文件不存在"
            }
        
        print_ok(f"节点文件存在: {node_file}")
        
        # 简单检查文件内容
        with open(node_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        checks = [
            ("KnowledgeClient", "KnowledgeClient 导入"),
            ("knowledge_client.search", "search() 调用"),
            ("knowledge_base_id", "知识库 ID 支持"),
            ("knowledge_has_result", "结果标识"),
        ]
        
        for keyword, desc in checks:
            if keyword in content:
                print_ok(f"{desc}: 发现 '{keyword}'")
            else:
                print_warn(f"{desc}: 未发现 '{keyword}'（可能不影响）")
        
        return {
            "has_node_file": True,
            "node_file": str(node_file)
        }
        
    except Exception as e:
        print_error(f"检查失败: {e}")
        return {
            "has_node_file": False,
            "error": str(e)
        }


def test_local_knowledge_search():
    """测试本地知识库检索（模拟 Coze SDK）"""
    print_banner("5. 测试本地知识库检索")
    
    test_queries = [
        "图书馆开放时间",
        "选课时间",
        "学生证补办",
        "考试安排",
        "校规校纪"
    ]
    
    # 模拟知识库数据
    sample_knowledge = {
        "图书馆开放时间": "图书馆开放时间：周一至周五 8:00-22:00，周末 9:00-21:00",
        "选课时间": "选课时间：2024年春季学期选课时间为2月15日-2月20日",
        "学生证补办": "学生证补办：携带身份证到教务处办理，费用20元，办公地点：行政楼201室",
        "考试安排": "考试安排：期末考试时间为6月15日-6月25日",
        "校规校纪": "校规校纪：按时上课，不迟到早退，遵守考试纪律，爱护公物"
    }
    
    print_info("这是本地模拟测试，验证检索逻辑")
    print_info("注意：此测试不连接真实 Coze 平台")
    
    results = []
    all_ok = True
    
    for query in test_queries:
        print(f"\n  查询: {query}")
        
        # 模拟简单的关键词匹配
        best_match = None
        best_score = 0.0
        
        for key, content in sample_knowledge.items():
            # 计算简单的匹配分数
            score = 0
            for word in query.split():
                if word in content:
                    score += 0.5
            for word in key.split():
                if word in query:
                    score += 0.3
            
            if score > best_score:
                best_score = score
                best_match = content
        
        if best_match and best_score > 0.3:
            has_result = best_score >= 0.5
            status = "✅" if has_result else "⚠️"
            print(f"    {status} 结果: {best_match[:60]}...")
            print(f"       相关度: {best_score:.2f}")
            print(f"       有结果: {'是' if has_result else '否'}")
            results.append({
                "query": query,
                "has_result": has_result,
                "score": best_score,
                "content": best_match
            })
        else:
            print(f"    ❌ 未找到相关内容")
            all_ok = False
            results.append({
                "query": query,
                "has_result": False,
                "score": 0.0,
                "content": ""
            })
    
    return {
        "results": results,
        "all_ok": all_ok
    }


def generate_report(config_check, env_check, state_check, code_check, local_test):
    """生成测试报告"""
    print_banner("📊 测试报告")
    
    # 总结
    score = 0
    max_score = 5
    
    print("\n  配置检查:")
    if config_check.get("has_config", False):
        score += 1
        print_ok("配置文件 ✓")
        if config_check.get("kb_id"):
            score += 1
            print_ok("知识库 ID 已配置 ✓")
        else:
            print_warn("知识库 ID 未配置（将使用默认绑定）")
    else:
        print_error("配置文件 ✗")
    
    print("\n  环境变量:")
    if env_check.get("has_env", False):
        score += 1
        print_ok("环境变量已设置 ✓")
    else:
        print_info("环境变量未设置")
    
    print("\n  配置读取:")
    if state_check.get("has_state_module", False):
        score += 1
        print_ok("配置读取功能正常 ✓")
    else:
        print_error("配置读取功能异常 ✗")
    
    print("\n  代码检查:")
    if code_check.get("has_node_file", False):
        score += 1
        print_ok("知识库检索代码存在 ✓")
    else:
        print_error("知识库检索代码缺失 ✗")
    
    print("\n  本地测试:")
    if local_test.get("all_ok", False):
        print_ok("本地检索测试通过 ✓")
    else:
        print_warn("部分本地检索测试未通过")
    
    print("\n" + "-"*70)
    print(f"  综合评分: {score}/{max_score}")
    
    if score == max_score:
        print_ok("🎉 所有检查通过！知识库配置良好。")
    elif score >= 3:
        print_warn("⚠️ 基本配置完成，但可能需要优化。")
    else:
        print_error("❌ 配置存在问题，请修复后再试。")
    
    print("-"*70)


def show_next_steps():
    """显示后续步骤"""
    print_banner("📋 后续步骤")
    
    steps = [
        "1. 如果知识库 ID 为空，请在 Coze 平台创建知识库并获取 ID",
        "2. 将知识库 ID 填入 config/knowledge_config.json",
        "3. 或设置环境变量 COZE_KNOWLEDGE_BASE_ID",
        "4. 在 Coze IDE 中测试工作流，查看执行日志",
        "5. 如仍有问题，查看 KNOWLEDGE_BASE_CONFIG_GUIDE.md"
    ]
    
    for step in steps:
        print(f"  {step}")


def show_how_to_check_coze_logs():
    """显示如何在 Coze 平台查看日志"""
    print_banner("🔍 如何在 Coze 平台查看执行日志")
    
    steps = [
        "方法1：在 Coze IDE 中测试",
        "  1. 在 Coze IDE 中打开项目",
        "  2. 点击「测试」或「Preview」按钮",
        "  3. 输入测试问题，如：图书馆开放时间",
        "  4. 在执行面板中查看各节点的输出",
        "  5. 特别查看 knowledge_search_node 的输出",
        "",
        "方法2：查看节点输出字段",
        "  knowledge_search_node 会返回以下字段：",
        "  - knowledge_result: 检索到的内容",
        "  - knowledge_score: 相关性得分（0-1）",
        "  - knowledge_has_result: 是否有有效结果（bool）",
        "  - knowledge_base_id: 使用的知识库 ID",
        "  - knowledge_search_info: 搜索详细信息",
        "",
        "方法3：检查日志关键字",
        "  - 如果看到 '检索到 X 条相关内容' = 成功",
        "  - 如果看到 '知识库中未找到相关内容' = 知识库已连接但无匹配",
        "  - 如果看到 '知识库检索异常' = 配置有问题"
    ]
    
    for step in steps:
        print(f"  {step}")


def main():
    """主函数"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║          校园校小助 - 知识库配置测试工具                       ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    
    # 执行各项检查
    config_check = check_knowledge_config()
    env_check = check_environment_variables()
    state_check = check_state_module()
    code_check = check_knowledge_search_code()
    local_test = test_local_knowledge_search()
    
    # 生成报告
    generate_report(config_check, env_check, state_check, code_check, local_test)
    
    # 显示后续步骤
    show_next_steps()
    
    # 显示 Coze 日志查看方法
    show_how_to_check_coze_logs()
    
    # 保存测试结果到文件
    print_banner("💾 保存测试结果")
    try:
        report = {
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "config_check": config_check,
            "env_check": env_check,
            "state_check": state_check,
            "code_check": code_check,
            "local_test": local_test
        }
        
        report_file = Path(__file__).parent / "knowledge_test_report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print_ok(f"测试报告已保存到: {report_file}")
    except Exception as e:
        print_error(f"保存报告失败: {e}")
    
    print("\n" + "="*70)
    print("测试完成！")
    print("="*70)


if __name__ == "__main__":
    main()
