"""
Adversarial robustness check for the vehicle detector — this week's
"Adversarial examples" slide (FGSM) applied concretely.

THE ATTACK: mock_detector.py decides "vehicle pixel" with a fixed rule —
r > 120 and r - g > 40 and r - b > 40. Because you can read that rule,
this is a WHITE-BOX attack, the same setting as slide 6's FGSM on a linear
model. There the attacker nudges every input by +/- eps in the direction
that hurts the model most (the sign of the gradient). Here that direction
is obvious from the rule: LOWER red, RAISE green and blue. A change of at
most `eps` per channel per pixel (an L-infinity budget) is visually tiny at
eps=10-20 on a 0-255 scale, yet pushes vehicle pixels across the rule's
boundary so the detector stops seeing them.

HONEST LIMITS: the mock detector is a hand-written colour rule, not a CNN,
so it is far more brittle than a trained detector, and the real attacks on
detectors (e.g. Eykholt et al.'s stickers) are physical and need gradients
through the network. What transfers is the METHOD: pick a perturbation
budget, attack, re-run the SAME audit, and report per-group damage. Not all
classes break at the same eps — and which ones break first is the finding.

Fill in the three functions marked # TODO.
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fairness_audit as fa


# ---------------------------------------------------------------------------
# Part 5 — The FGSM-style perturbation
# ---------------------------------------------------------------------------

def perturb_image(img, eps):
    """`img` is an RGB PIL Image, `eps` an int >= 0 (the L-infinity budget).

    Return a NEW RGB image where every pixel has: red lowered by eps, green
    raised by eps, blue raised by eps — each channel clamped to [0, 255].
    Do not modify `img` in place. eps=0 must return an identical image.

    Hint: Image.split() gives the three channels; Image.point(fn) applies a
    function to every value of a single-channel image; Image.merge("RGB",
    ...) puts them back. No per-pixel Python loop is needed.
    """
    # TODO: implement
    image = img.convert("RGB")

    red, green, blue = image.split()

    red = red.point(lambda value: max(0, value - eps))
    green = green.point(lambda value: min(255, value + eps))
    blue = blue.point(lambda value: min(255, value + eps))

    return Image.merge("RGB", (red, green, blue))


# ---------------------------------------------------------------------------
# Part 6 — Re-run the audit under attack
# ---------------------------------------------------------------------------

def audit_under_attack(coco_path, fixtures_dir, eps_values=(0, 10, 20, 30, 40),
                       iou_threshold=0.3):
    """For each eps in `eps_values`, run audit_by_category on images that
    have been perturbed with perturb_image(img, eps) (use the `transform`
    argument of audit_by_category — that is what it is for).

    Return {eps: category_stats}, where category_stats is exactly what
    audit_by_category returns. eps=0 is the clean audit.
    """
    # TODO: implement
    attack_stats = {}

    for eps in eps_values:
        def transform(image, budget=eps):
            return perturb_image(image, budget)

        category_stats = fa.audit_by_category(
            coco_path,
            fixtures_dir,
            iou_threshold=iou_threshold,
            transform=transform
        )

        attack_stats[eps] = category_stats

    return attack_stats


# ---------------------------------------------------------------------------
# Part 7 — Which classes are the most fragile?
# ---------------------------------------------------------------------------

def find_most_fragile(attack_stats, eps, top_k=3):
    """`attack_stats` is the dict returned by audit_under_attack and must
    contain eps=0 (clean) and the given `eps`.

    For every category, compute drop = recall at eps=0 minus recall at
    `eps`. Return the `top_k` categories with the LARGEST drop as a list of
    (category_name, drop) tuples, biggest drop first; break ties by
    category name (alphabetical). Round drop to 4 decimal places.

    Note: with only ~5-30 boxes per class, the drop ranking is noisy and can
    change with the student ID. run_pipeline.py also reports the classes with
    the lowest ABSOLUTE recall under attack; compare the two in NOTES.md.
    """
    clean_stats = attack_stats[0]
    attacked_stats = attack_stats[eps]

    recall_drops = []

    for category_name, clean_data in clean_stats.items():
        if category_name not in attacked_stats:
            continue
        
        clean_recall = clean_data["recall"]
        attacked_recall = attacked_stats[category_name]["recall"]

        drop = clean_recall - attacked_recall

        recall_drops.append((category_name, round(drop, 4)))

    recall_drops.sort(key=lambda item: (-item[1], item[0]))

    return recall_drops[:top_k]
