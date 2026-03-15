# Day 16 AM Part D — AI-Augmented Task (Type I & Type II in fraud detection)

## Prompt used

"Explain Type I and Type II errors in the context of a fraud detection system. What are the real-world consequences of each, and how do you balance them?"

## Documented output (summary)

- **Type I error (false positive):** Rejecting the null when it is true. In fraud detection: flagging a legitimate transaction as fraud. Consequences: declined valid customers, lost sales, poor UX, support cost, customer churn.
- **Type II error (false negative):** Failing to reject the null when it is false. In fraud detection: failing to flag a fraudulent transaction. Consequences: financial loss, chargebacks, reputational damage.
- **Balancing:** Lowering the decision threshold reduces Type I (fewer false alarms) but increases Type II (more fraud slips through). Raising the threshold does the opposite. The balance depends on cost of each error (e.g. cost of a false decline vs cost of one undetected fraud). Precision–recall tradeoff: Type I relates to precision (fewer false positives → higher precision), Type II to recall (catching more fraud → higher recall); tuning the threshold trades off precision and recall.

## Evaluation

- **Does the AI correctly explain the precision–recall tradeoff as the Type I/II error tradeoff?** Yes — if the AI output states that reducing false positives (Type I) improves precision and reducing false negatives (Type II) improves recall, and that changing the classification threshold trades off the two, that is a correct link. Type I = false positive rate ↔ precision (and specificity); Type II = false negative rate ↔ recall (sensitivity). So “balancing Type I and Type II” corresponds to choosing a point on the precision–recall curve. The evaluation should note whether the AI made this link explicit; if so, the answer is satisfactory.
