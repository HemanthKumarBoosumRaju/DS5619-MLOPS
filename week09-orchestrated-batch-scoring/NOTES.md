# NOTES.md — Week 9: Orchestrated Batch Scoring

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->

student_id: 142602003
seed: 563654705
## notify retry count

<!-- How many attempts did notify take in your run? (Check
     dag_run_summary.json.) -->
3

## Branch independence

<!-- Why does load still succeed even though notify — its "sibling" in the
     DAG — failed on its first two attempts? What does that tell you about
     how failures in one branch of a DAG should (or shouldn't) affect an
     unrelated branch? -->
load still succeeds because load and notify are separate branches of the DAG. Both depend on score, but load does not depend on notify.

So when notify fails, it does not affect load. A failure should only prevent tasks that depend on the failed task from running. An unrelated branch should be allowed to continue if its own dependencies have succeeded. 

## Retry cost under FinOps

<!-- Tying back to this week's FinOps content: if notify were a metered API
     call you paid for per attempt, what would you change about the retry
     strategy, and why is "retry every failed task the same way" a risky
     default once cost enters the picture? -->
If notify were a paid API call, I would use fewer retries and a longer delay between attempts. I would retry only when the failure is likely to be temporary.

Every retry means another API call and another cost. For example, two retries can result in three paid API calls.

Using the same retry settings for every task is risky because tasks have different costs and types of failures. A cheap local task can be retried more, but an expensive API call should have fewer retries. The retry strategy should balance reliability with cost.