# Methodology

## What to ask for

Ask for whatever is missing, a few items at a time.

### For every project

- **Problem formulation:** inputs, outputs and objective
- **Pipeline or architecture:** the stages, in order
- **Tools:** languages, frameworks and libraries (with versions), and hardware
- **Experimental setup:** how the work is evaluated, the metrics, the baselines and how many runs
- **What is theirs and what is reused:** this matters for honest claims about the contribution

### ML / deep learning

- **Dataset:** name, source link, licence, size, classes and class balance; how it was collected if it's their own
- **Preprocessing and augmentation,** and whether these were applied before or after splitting the data. Applying them before the split leaks test information into training.
- **Split:** train, validation and test ratios; stratification; cross-validation. Split by subject, patient or time when samples from the same source must not appear on both sides.
- **Model:** architecture, pretrained weights, layers changed, loss function, optimiser, learning rate, batch size, epochs and early stopping
- **Hyperparameter tuning:** how it was done, which must be on the validation set, never the test set
- **Baselines:** at least two relevant ones, run by the student under the same protocol

### IoT / embedded / hardware

- **Block diagram:** sensors (with model numbers), microcontroller, communication (Wi-Fi, LoRa, BLE, MQTT), cloud and app
- Circuit and connection details, power supply and sensor calibration
- **Deployment:** where, for how long, and how many readings
- **Evaluation:** error against a reference instrument, latency, battery life, packet loss and cost

### Software systems / web / apps

- Architecture (client and server, database, APIs) and the key algorithms
- **Evaluation:** performance (response time, throughput) under a stated load; a usability study with the number of participants and the instrument used (for example SUS); comparison with existing tools

### Simulation and analytical work (ECE, EE, ME, Civil)

- Governing equations or models, and the assumptions behind them
- Tool and version (MATLAB/Simulink, ANSYS, COMSOL, NS-3 and so on), with mesh and parameter settings
- **Validation:** against an analytical result, experimental data or a published benchmark (verified)
- Parameter sweeps or sensitivity analysis

### Experimental work in core branches

- Materials, specimen preparation, and the standards followed (for example ASTM or IS codes). Check each standard's number and title live before citing it.
- Equipment, number of samples and repeats, and measurement uncertainty

## Section structure

Adapt this to the template:

1. **Overview:** one paragraph and a system or block diagram
2. **Dataset, materials or setup**
3. **Proposed method:** a subsection for each component, with equations and pseudocode where they help
4. **Implementation details:** a parameter and value table
5. **Evaluation protocol:** metrics (with formulas if they aren't standard), baselines and splits

The student should draw the block diagram cleanly in draw.io or PowerPoint, or generate it with Mermaid or TikZ. Screenshots of code don't belong in the figure.

## Strengthening (Stage 3)

Roughly ordered by how much reviewers care:

| Problem | Fix | Effort |
|---|---|---|
| No baseline | Run two standard baselines on the same split | Low to medium |
| Accuracy is the only metric | Add precision, recall and F1 (macro-averaged for imbalanced classes) and a confusion matrix; RMSE and MAE for regression; the usual metrics for the domain | Low |
| Possible data leakage (augmentation or normalisation before the split, duplicates across splits, the same patient in train and test) | Re-split properly and re-run | Medium |
| Only one run | Report mean ± standard deviation over 3 to 5 random seeds, or use k-fold cross-validation | Low to medium |
| The method is the same as an existing paper | Find a genuine difference (setting, data, constraint), or reframe honestly as a comparative or replication study | Medium |
| Choices aren't justified | Justify each key choice with a verified citation or a small comparison | Low |
| No ablation study | Remove one component at a time and measure the effect | Medium |
| Lab data only | Add a small real-world test set, or test on a second dataset | Medium to high |
| A hardware project with no evaluation | Measure against a reference instrument and report error, latency, power and cost | Medium |
| Scope too large for the deadline | Cut it to the part that can be evaluated properly | Low |

Rules for suggestions:

- Only suggest what fits before the deadline.
- When recommending a technique, cite a verified paper.
- The student does the implementation.
- Anything that can't be fixed goes into the Limitations section, stated honestly.
