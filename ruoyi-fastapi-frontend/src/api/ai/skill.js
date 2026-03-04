import request from "@/utils/request";

// 查询技能列表
export function getSkillList() {
  return request({
    url: "/ai/skill/list",
    method: "get",
  });
}

// 查询技能详细
export function getSkillDetail(skillName) {
  return request({
    url: "/ai/skill/detail/" + skillName,
    method: "get",
  });
}

// 查询技能统计
export function getSkillStats() {
  return request({
    url: "/ai/skill/stats",
    method: "get",
  });
}

// 获取技能提示词（调试用）
export function getSkillPrompt() {
  return request({
    url: "/ai/skill/prompt",
    method: "get",
  });
}
