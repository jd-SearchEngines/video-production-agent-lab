# v0.3 Skill Comparison

Run ID: `v03-20260904T193146Z`

{
  "one_large_prompt": {
    "task_success_rate": 0.16666666666666666,
    "mean_instruction_violations": 0.8333333333333334
  },
  "stage_skills": {
    "task_success_rate": 1.0,
    "mean_instruction_violations": 0.0
  }
}

The baseline and treatment use the same six deterministic fixtures. Stage skills are loaded from independent Markdown files and the scripted local model boundary is not a real LLM call; provider/model/token/cost fields are therefore null.
