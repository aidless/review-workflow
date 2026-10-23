import sys
import time

sys.path.insert(0, r"F:\deepseek\research-kit")
import adversarial_review as adv

adv.RPC = "http://127.0.0.1:3080"

# Test 1: medium-length prompt (300 chars)
p1 = "你是数字对账审稿人。论文中有一个小数无法在产物 JSON 中机械匹配到支撑。请裁决该数字的性质：noise（误报）/ supported（实质断言且有来源）/ critical（实质断言但无来源）。数字：0.355。请输出严格 JSON。"
print(f"test1 len={len(p1)}", flush=True)
t0 = time.time()
rec = adv.prompt_turn(p1, "r3-probe", timeout=120)
print(f"test1 took {time.time()-t0:.1f}s, status={rec['status']}", flush=True)
print("  raw head:", (rec.get("raw") or "")[:150], flush=True)

# Test 2: short English prompt
p2 = "Classify this number as noise, supported, or critical. Number: 0.355. Output JSON only."
print(f"test2 len={len(p2)}", flush=True)
t0 = time.time()
rec = adv.prompt_turn(p2, "r3-probe", timeout=120)
print(f"test2 took {time.time()-t0:.1f}s, status={rec['status']}", flush=True)
print("  raw head:", (rec.get("raw") or "")[:150], flush=True)
