# KukuFiti Framework — Godmode Enhancement
## Complete Operational Intelligence Supplement

> **Document Purpose:** This supplement extends the KukuFiti Architectural and Agronomic Blueprint with the complete operational layer required for production-grade farm intelligence. The original document (Sections 1–7) establishes the biological baseline, anomaly thresholds, economic model, and core schema. This supplement fills every gap between that blueprint and a real, deployable farm system — covering the 48 hours before a chick is placed through the post-harvest inter-batch machine learning loop.

---

# PART I: FOUNDATIONAL ARCHITECTURE

## Section 1: Lifecycle Breakdown (Core Foundation)

The modern broiler chicken possesses immense genetic potential for rapid tissue accretion, capable of multiplying its hatch weight by a factor of seventy within six weeks. To translate this biological potential into a robust backend data structure, the 42-day lifecycle must be discretized into four distinct physiological phases. Each phase dictates highly specific environmental parameters, nutritional requirements, and expected performance benchmarks that the KukuFiti system must continuously track and evaluate against live sensor telemetry.

### Phase 1: Brooding (Day 0–7)

The brooding phase represents the most critical period in the broiler lifecycle, dictating the ultimate trajectory of the flock's cardiovascular, skeletal, and immunological development. At the moment of placement, a day-old chick is functionally poikilothermic; it lacks the capacity to internally regulate its body temperature and relies entirely on external thermal energy sources provided by the housing infrastructure. Furthermore, the rapid biological transition from utilizing internal yolk sac lipid reserves to digesting and absorbing exogenous carbohydrate-protein feed requires precise management of both ambient temperature and feed structure.

The environmental requirements during this initial phase are stringent. Day 0 commences at an ambient air temperature at chick level of 32.0°C to 36.0°C, strictly contingent on the concurrent relative humidity, to maintain a target internal chick body temperature of 39.5°C to 40.5°C. This ambient temperature must be reduced gradually, approximating a drop of 0.5°C per day, until it reaches 30.0°C to 31.0°C by Day 7. Relative humidity during the first three days must be maintained tightly between 60% and 70% to prevent rapid dehydration and to support the delicate respiratory mucosa, before being allowed to drop toward 60% by the end of the first week. Minimum ventilation is an absolute necessity from the moment of placement, not for temperature control, but to exhaust noxious waste gases. The ventilation infrastructure must clear carbon dioxide, ensuring it remains below 3000 parts per million (ppm), and exhaust ammonia to levels below 10 ppm, requiring a continuous mechanical air exchange rate of 0.10 cubic feet per minute (CFM) per bird. The lighting schedule initiates with 24 hours of continuous, high-intensity illumination (approximately 11 to 20 lux) for the first 48 hours to stimulate the chicks' curiosity and ensure immediate discovery of feed and water sources. Following this initial period, a strict circadian rhythm is established by introducing a minimum of one hour of continuous darkness, which assists in immunological development.

Feeding and hydration protocols must be optimized for rapid prehension and digestion. The nutritional input must be a highly digestible Starter feed, processed into a sieved crumble format with a diameter of roughly 2 millimeters to facilitate easy consumption by small beaks. This starter diet is exceptionally nutrient-dense, requiring 21% to 22% crude protein, 1.22% digestible lysine, and 12.45 MJ/kg of metabolizable energy to support the explosive initial growth of internal organs and the skeletal frame. Daily feed intake per bird begins at a minuscule 13 to 14 grams on Day 1, escalating rapidly to roughly 34 to 40 grams by Day 7, resulting in a target total cumulative feed consumption of 180 to 220 grams per bird by the end of the phase. Water consumption is highly correlated with feed intake, operating at a water-to-feed volumetric ratio of roughly 1.8:1 to 2.0:1 during the first week. To ensure consumption, the water temperature must be maintained strictly between 18.0°C and 21.0°C; if the water temperature exceeds 30.0°C, chicks will significantly reduce their intake, leading to cascading failures in feed consumption and growth.

The biological performance benchmarks for the brooding phase are steep. A healthy Cobb 500 or Ross 308 bird is expected to achieve 4.5 to 5.0 times its initial hatch weight, targeting an absolute mass of 202 to 240 grams by Day 7. The expected cumulative feed conversion ratio (FCR) is highly efficient during this period of hyper-growth, approximating 0.89. Mortality naturally peaks during this first week due to genetic culling, yolk sac infections, and transportation stress; therefore, an aggregate mortality rate of up to 1.54% is considered the acceptable industry benchmark for the entirety of Phase 1.

| Phase 1 Parameters | Target Value |
|---|---|
| Start / End Weight | 42g / 202g |
| Daily Temperature Range | 36.0°C (Day 0) decreasing to 30.0°C (Day 7) |
| Target Humidity | 60% - 70% |
| Ventilation Target | 0.10 CFM per bird |
| Dietary Profile | Starter Crumble (21-22% Crude Protein, 12.45 MJ/kg) |
| Cumulative Feed Intake | 180g - 220g per bird |
| Water-to-Feed Ratio | 1.8:1 to 2.0:1 |
| Acceptable Mortality | ≤1.54% cumulative for the week |

### Phase 2: Early Growth (Day 8–14)

As the flock enters the second week of life, the birds begin to develop their own internal thermoregulatory capabilities, transitioning away from complete reliance on external brooders. This phase is characterized by the rapid expansion of the skeletal frame and the emergence of primary feathers. However, this hyper-accelerated growth introduces the first major biological risks to the flock; if muscular and skeletal growth outpaces the concurrent development of the cardiovascular and pulmonary systems, the birds become highly susceptible to metabolic disorders such as Sudden Death Syndrome (SDS) and early-onset ascites.

The physical environment must adapt to accommodate the increasing metabolic heat generated by the growing flock biomass. Ambient temperature set-points must be progressively reduced from 30.0°C on Day 8 down to 27.0°C by Day 14. Relative humidity must be tightly clamped between 50% and 60%; as the birds excrete larger volumes of feces and respired moisture, exceeding 60% humidity rapidly degrades litter quality, establishing a vector for coccidiosis parasites. To extract this compounding moisture and the rising levels of metabolic carbon dioxide, the ventilation system must be linearly scaled up, shifting from 0.10 CFM to 0.25 CFM per bird by the conclusion of Day 14. The lighting program during this phase often incorporates an extended darkness period—ranging from four to six hours depending on specific farm management strategies—which physically forces the birds to rest, intentionally slowing their feed intake to allow cardiovascular development to synchronize with muscle accretion.

Nutritionally, the KukuFiti system must log a shift in the feed inventory from the Starter diet to a Grower diet, which is typically presented as a larger crumble or a micro-pellet to improve ingestion efficiency. The formulation shifts slightly, reducing crude protein to a range of 19% to 20% while elevating the metabolizable energy density to 12.66 MJ/kg. Daily feed consumption accelerates dramatically, climbing from roughly 40 grams per bird on Day 8 to 80 grams per bird by Day 14. Consequently, the cumulative feed logged by the end of the second week should reach approximately 588 grams per bird. Water consumption stabilizes near a 1.7:1 or 1.8:1 ratio to the mass of feed consumed, requiring backend IoT systems to verify that water line pressure has been increased to deliver between 60 and 70 milliliters per minute from each nipple drinker.

Performance benchmarks require the flock to achieve an average live weight of approximately 400 to 570 grams by Day 14. With the weakest birds having succumbed during the brooding phase, the mortality baseline flattens significantly. The backend anomaly detection engine should expect a stabilized, low-level attrition rate not exceeding 0.48% for the entire week.

| Phase 2 Parameters | Target Value |
|---|---|
| Start / End Weight | 240g / 570g |
| Daily Temperature Range | 30.0°C (Day 8) decreasing to 27.0°C (Day 14) |
| Target Humidity | 50% - 60% |
| Ventilation Target | 0.25 CFM per bird |
| Dietary Profile | Grower Crumble/Pellet (19-20% Crude Protein, 12.66 MJ/kg) |
| Cumulative Feed Intake | 588g per bird (Total from Day 0) |
| Water Nipple Flow Rate | 60 - 70 ml/min |
| Acceptable Mortality | ≤0.48% cumulative for the week |

### Phase 3: Mid Growth (Day 15–28)

The third phase marks the absolute peak of the biological growth curve's acceleration. During this two-week period, skeletal development slows, and the physiological priority shifts entirely toward massive muscular hypertrophy, particularly in the breast tissue. The bird's cardiovascular and respiratory systems are now operating near their maximum theoretical limits to supply oxygen to this rapidly expanding muscle mass. Consequently, the flock's susceptibility to severe heat stress, hypoxia, and subsequent cardiac failure reaches its zenith, requiring the KukuFiti environmental monitoring logic to operate with zero tolerance for deviations.

The environmental control logic must execute a continuous, aggressive reduction in ambient temperature, stepping down from 27.0°C to the flock's terminal thermal comfort zone of 20.0°C to 21.0°C by Day 28. If the backend sensors detect temperatures exceeding 21.0°C beyond Day 21, the system must recognize that feed intake and ultimate growth rates will be heavily penalized as the birds stop eating to minimize the thermic effect of digestion. Relative humidity must remain clamped between 50% and 60% to prevent the litter from capping (forming a hard, wet crust), which instantly triggers painful pododermatitis (footpad lesions) and fosters severe bacterial loads. To manage the massive volume of respired heat and atmospheric moisture generated by a shed containing thousands of birds, the mechanical ventilation requirement doubles, scaling from 0.35 CFM per bird on Day 15 to a minimum of 0.50 CFM per bird by Day 28.

Feeding regimens transition to a Finisher 1 diet, or a continuation of the Grower diet, strictly presented in a pelleted format to minimize energy expended during eating. The dietary formulation continues its trajectory of dropping crude protein (18% to 19%) while boosting energy content (12.97 MJ/kg) to fuel pure tissue volume expansion. The volume of feed processed by the farm reaches industrial scales; daily intake per bird surges from 84 grams to 165 grams over this period, pushing the cumulative lifecycle feed consumption to a massive 2,359 grams per bird by Day 28. Concurrently, the absolute volume of water consumed increases exponentially, mandating that the physical nipple drinkers deliver flow rates approaching 70 to 100 milliliters per minute to prevent dehydration and support the metabolism of the heavy feed load.

The target performance metrics establish a critical milestone: the flock must achieve an average live weight of roughly 1,400 to 1,783 grams by Day 28. The expected mortality rate remains benchmarked at ≤0.48% per week. Spikes in mortality detected by the KukuFiti system during this phase are almost exclusively linked to right ventricular failure (ascites) resulting from insufficient ventilation or extreme heat stress.

| Phase 3 Parameters | Target Value |
|---|---|
| Start / End Weight | 639g / 1,783g |
| Daily Temperature Range | 27.0°C (Day 15) decreasing to 20.0°C (Day 28) |
| Target Humidity | 50% - 60% |
| Ventilation Target | 0.35 to 0.50 CFM per bird |
| Dietary Profile | Finisher 1 Pellet (18-19% Crude Protein, 12.97 MJ/kg) |
| Cumulative Feed Intake | 2,359g per bird (Total from Day 0) |
| Water Nipple Flow Rate | 70 - 100 ml/min |
| Acceptable Mortality | ≤0.48% cumulative per week |

### Phase 4: Finishing (Day 29–Harvest, Day 35-42)

The final stage of the production cycle is dedicated entirely to maximizing the ultimate harvest yield while fiercely defending the accumulated economic investment against late-stage mortality. Biological management shifts away from promoting growth—which is now driven by sheer momentum—and focuses almost entirely on avoiding heat stress, maintaining optimal air quality, and preparing the birds' digestive tracts for processing and slaughter.

Environmental management during the finishing phase is a delicate exercise in thermal extraction. Because the sheer density of bird biomass in the housing prevents natural heat dissipation, ambient temperatures must be maintained stringently between 18.0°C and 20.0°C. Relative humidity must be strictly policed below 60%. The thermodynamic concept of enthalpy becomes the primary threat vector; if humidity rises concurrently with high ambient temperatures, the moisture-laden air prevents the birds from utilizing evaporative cooling via panting. When enthalpy limits are breached, core body temperatures spiral, leading to mass mortality events within hours. To prevent this, the KukuFiti logic must ensure ventilation rates operate at absolute maximums, demanding 0.65 to 0.70 CFM per bird in standard conditions, and potentially up to 0.90 CFM per bird in extreme heat, often necessitating the actuation of tunnel ventilation and evaporative cooling pad infrastructure.

The nutritional program utilizes a Finisher 2 diet, exclusively in pellet form, representing the lowest protein concentration (17% to 18%) and the highest metabolizable energy density (13.18 MJ/kg) to maximize final intramuscular fat deposition and total carcass yield. The daily feed intake curve begins to plateau, moving slowly from 169 grams to approximately 220 grams per bird daily. By the point of harvest at Day 42, cumulative feed intake will reach an immense 4,405 to 5,100 grams per bird. Water consumption drops slightly relative to feed volume, settling near a 1.6:1 ratio, but remains at absolute peak volumetric flow to sustain the heavy biological load.

The ultimate performance benchmarks define the success of the entire enterprise. A standard Cobb 500 or Ross 308 flock should clear a harvest weight of 2,521 grams if slaughtered early at Day 35, or achieve an astonishing 3,278 grams if taken to the full Day 42 cycle. The final cumulative Feed Conversion Ratio (FCR) should land securely within a highly efficient range of 1.50 to 1.65, heavily dependent on late-stage mortality rates and feed wastage mitigation.

| Phase 4 Parameters | Target Value |
|---|---|
| Start / End Weight | 1,886g / 3,278g |
| Daily Temperature Range | 20.0°C to 18.0°C (Strictly maintained) |
| Target Humidity | < 60% (Crucial for enthalpy control) |
| Ventilation Target | 0.65 to 0.70 CFM per bird (up to 0.90 in heat) |
| Dietary Profile | Finisher 2 Pellet (17-18% Crude Protein, 13.18 MJ/kg) |
| Cumulative Feed Intake | 5,100g per bird (Total from Day 0) |
| Target Final FCR | 1.50 to 1.65 |
| Acceptable Mortality | ≤0.48% cumulative per week |

---

## Section 2: Daily Target Model (The KukuFiti Baseline Data Matrix)

For the FastAPI backend to execute meaningful mathematical anomaly detection, it requires an absolute, deterministic source of truth. This source of truth takes the form of a baseline reference curve against which all daily sensor telemetry and manual farm inputs are continuously compared. The following dataset synthesizes the biological targets for a standard high-yield broiler (utilizing the Cobb 500 As-Hatched Metric performance objectives as the primary genetic baseline) distributed across a 42-day cycle.

This structured matrix maps directly to the backend relational database, specifically populating the table schema defined as:

```sql
batch_targets(day_number, target_weight_g, daily_gain_g, daily_feed_g, cumulative_feed_g, target_water_ml, target_temp_c, expected_daily_mortality_pct)
```

The `target_water_ml` metric is dynamically calculated by the backend using a standard biological multiplier of 1.8x the mass of the daily feed intake, a recognized standard for ideal temperature conditions. The `expected_daily_mortality_pct` is derived from standard actuarial decay curves in poultry production, front-loading the expected 1.54% first-week mortality before smoothing out to a daily fraction of the 0.48% weekly allowance for the remainder of the cycle.

| Day | Target Weight (g) | Daily Gain (g) | Daily Feed (g) | Cum. Feed (g) | Target Water (ml) | Target Temp (°C) | Expected Mortality (%) |
|---|---|---|---|---|---|---|---|
| 0 | 42 | - | - | - | - | 34.0 | 0.25 |
| 1 | 55 | 13 | 14 | 14 | 25 | 33.5 | 0.25 |
| 2 | 71 | 16 | 17 | 31 | 31 | 33.0 | 0.22 |
| 3 | 90 | 19 | 20 | 51 | 36 | 32.5 | 0.22 |
| 4 | 112 | 22 | 24 | 75 | 43 | 32.0 | 0.20 |
| 5 | 138 | 26 | 28 | 103 | 50 | 31.5 | 0.20 |
| 6 | 168 | 30 | 33 | 136 | 59 | 31.0 | 0.20 |
| 7 | 202 | 34 | 40 | 180 | 72 | 30.0 | 0.20 |
| 8 | 240 | 38 | 40 | 220 | 72 | 29.5 | 0.08 |
| 9 | 283 | 43 | 44 | 264 | 79 | 29.0 | 0.08 |
| 10 | 330 | 47 | 50 | 314 | 90 | 28.5 | 0.07 |
| 11 | 382 | 52 | 57 | 371 | 103 | 28.0 | 0.07 |
| 12 | 440 | 58 | 64 | 435 | 115 | 27.5 | 0.06 |
| 13 | 503 | 63 | 73 | 508 | 131 | 27.0 | 0.06 |
| 14 | 570 | 67 | 80 | 588 | 144 | 26.5 | 0.06 |
| 15 | 639 | 69 | 84 | 672 | 151 | 26.0 | 0.06 |
| 16 | 711 | 72 | 91 | 763 | 164 | 25.5 | 0.06 |
| 17 | 786 | 75 | 98 | 861 | 176 | 25.0 | 0.06 |
| 18 | 864 | 78 | 105 | 966 | 189 | 24.5 | 0.06 |
| 19 | 945 | 81 | 111 | 1077 | 200 | 24.0 | 0.06 |
| 20 | 1029 | 84 | 118 | 1195 | 212 | 23.5 | 0.06 |
| 21 | 1116 | 87 | 125 | 1320 | 225 | 23.0 | 0.06 |
| 22 | 1205 | 89 | 131 | 1451 | 236 | 22.5 | 0.06 |
| 23 | 1296 | 91 | 137 | 1588 | 247 | 22.0 | 0.06 |
| 24 | 1390 | 94 | 143 | 1731 | 257 | 21.5 | 0.06 |
| 25 | 1486 | 96 | 149 | 1880 | 268 | 21.0 | 0.06 |
| 26 | 1583 | 97 | 154 | 2034 | 277 | 20.5 | 0.06 |
| 27 | 1682 | 99 | 160 | 2194 | 288 | 20.0 | 0.06 |
| 28 | 1783 | 101 | 165 | 2359 | 297 | 20.0 | 0.06 |
| 29 | 1886 | 103 | 169 | 2528 | 304 | 20.0 | 0.06 |
| 30 | 1989 | 103 | 174 | 2702 | 313 | 20.0 | 0.06 |
| 31 | 2094 | 105 | 178 | 2880 | 320 | 20.0 | 0.06 |
| 32 | 2200 | 106 | 183 | 3063 | 329 | 20.0 | 0.06 |
| 33 | 2306 | 106 | 187 | 3250 | 337 | 20.0 | 0.06 |
| 34 | 2413 | 107 | 191 | 3441 | 344 | 20.0 | 0.06 |
| 35 | 2521 | 108 | 194 | 3635 | 349 | 20.0 | 0.06 |
| 36 | 2629 | 108 | 198 | 3833 | 356 | 20.0 | 0.06 |
| 37 | 2738 | 109 | 202 | 4035 | 364 | 20.0 | 0.06 |
| 38 | 2846 | 108 | 206 | 4241 | 371 | 20.0 | 0.06 |
| 39 | 2954 | 108 | 209 | 4450 | 376 | 20.0 | 0.06 |
| 40 | 3062 | 108 | 213 | 4663 | 383 | 20.0 | 0.06 |
| 41 | 3170 | 108 | 217 | 4880 | 391 | 20.0 | 0.06 |
| 42 | 3278 | 108 | 220 | 5100 | 396 | 20.0 | 0.06 |

---

## Section 3: Deviation & Anomaly Detection

Precision agriculture relies implicitly on the capability to identify statistical deviations from the established baseline before biological failure—such as clinical disease, mass mortality, or chronic physiological stress—manifests visually on the farm floor. The KukuFiti system acts as a digital twin of the broiler flock, running constant telemetry inputs through detection algorithms. While simple threshold gating provides a baseline, advanced implementations utilize Isolation Forests and moving average calculations to filter out sensor noise and trigger actionable, highly specific alerts.

The following logical thresholds and biological rationales formulate the core intelligence grid for the backend application.

### 3.1 Feed Intake Deviation

Because birds will naturally and immediately modulate their feed intake based on thermal comfort and impending disease vectors, daily feed consumption serves as the primary "soft sensor" for overall flock health. A broiler chicken will invariably stop eating before it shows clinical signs of illness.

| Threshold | Definition |
|---|---|
| **Acceptable Range** | Variance of ±5% from the daily target metric |
| **Warning Threshold** | Drop between −5% and −10% compared to target curve (~7–9g/bird/day) |
| **Critical Threshold** | Drop exceeding >10%, or complete flattening of cumulative feeding curve over 48-hour period |

**Likely Causes:** Severe heat stress (primary cause — birds halt eating to reduce thermic effect of digestion). If temperatures normal: impending viral outbreak (Newcastle Disease, Avian Influenza — sudden, flock-wide anorexia), mycotoxin-contaminated feed, or mechanical failure in water lines.

**System Action:** Immediately query local environmental sensors. If ambient temperature normal → high-priority alert to inspect water nipple pressure. If water adequate → automated recommendation for urgent veterinary pathological review.

### 3.2 Water-to-Feed Ratio Deviation

Volumetric water consumption tracking is highly predictive of physiological distress. Research demonstrates that drops of merely 14 ml to 18 ml below the daily expected water target serve as early precursors to mortality events. Conversely, massive spikes in water consumption indicate severe thermal or intestinal stress.

| Threshold | Definition |
|---|---|
| **Acceptable Range** | Dynamic ratio of 1.6:1 up to 1.8:1 (water volume to feed mass) |
| **Warning Threshold** | Ratio spiking above >2.0:1 or dropping below <1.5:1 |
| **Critical Threshold** | Ratio exceeding >2.5:1 or collapsing below <1.2:1 |

**Likely Causes — High Ratio (>2.0:1):** Severe heat stress (birds ingest massive water quantities to fuel evaporative cooling via panting) OR enteritis/coccidiosis outbreak (severe diarrhea causes desperate compensatory drinking).

**Likely Causes — Low Ratio (<1.5:1):** Mechanical blockage in nipple lines; water temperature exceeding 30.0°C (birds refuse to drink); cold stress causing huddling instead of water-seeking.

**System Action:** Cross-reference temperature telemetry. If elevated → actuate secondary cooling fans/fogging systems via IoT. If normal → critical maintenance alert to manually flush water lines and check pump pressure.

### 3.3 Mortality Rate Spikes

Normal baseline mortality operates on a predictable decay curve — relatively high in Week 1 due to genetic culling and transportation stress, then flattening to an incredibly low daily rate of <0.1% per day. Any deviation from this decay curve is an emergency.

| Threshold | Definition |
|---|---|
| **Acceptable Range** | Within expected daily target from batch matrix (e.g., <0.06% on Day 20) |
| **Warning Threshold** | Daily mortality ≥0.25% for a single 24-hour period |
| **Critical Threshold** | Daily mortality ≥0.5% for single day, OR daily count exceeding >2.9× the historical moving average |

**Likely Causes:** Sudden explosive outbreaks of highly virulent pathogens (Gumboro/IBD, Newcastle Disease). Non-pathological: catastrophic temperature failure (power outage → asphyxiation), late-stage Hypoxia/Ascites in high-altitude environments.

**System Action:** **CRITICAL ALERT.** Backend instantiates biosecurity lockdown protocol across application UI, warning against personnel/equipment movement. System prompts farm manager to input qualitative mortality causes (e.g., "birds flipped on backs", "bloody feces") to aid immediate veterinary diagnostics.

### 3.4 Body Weight & FCR Deviation

Live body weight is continuously estimated via automated step-on load cells distributed throughout the poultry house, or via daily manual sampling inputted into the application. The Feed Conversion Ratio is recalculated continuously.

| Threshold | Definition |
|---|---|
| **Acceptable Range** | Live weight within ±5% of target matrix. FCR within ±0.05 of genetic benchmark |
| **Warning Threshold** | >5% negative deviation in body weight, OR cumulative FCR climbing above 1.70 during Phase 3 or 4 |
| **Critical Threshold** | >10% negative deviation in weight, OR FCR spiraling above 1.85 |

**Likely Causes:** Substandard feed formulation lacking highly digestible amino acids (primary culprit). Biological: chronic subclinical coccidiosis (destroys intestinal villi, prevents nutrient absorption), chronic cold stress (forces bird to metabolize feed energy into heat rather than muscle deposition).

**System Action:** Flag specific feed supplier ID used for this batch for immediate quality and procurement review. Simultaneously suggest temporary 1.0°C increase in ambient temperature set-points to eliminate possibility of chronic cold stress.

---

## Section 4: Decision Engine Rules (Backend Logic)

To transform biological knowledge and threshold matrices into a functional API, the system requires a rigidly defined rules engine. This engine is designed to process incoming JSON telemetry logs in real-time, evaluating complex conditional probabilities across multiple data streams. The backend logic is encapsulated in discrete algorithmic rules, optimized to be executed via scheduled background tasks (e.g., Celery workers in Python or native FastAPI background routines).

### Rule 1: The Cold Stress & Chilling Protocol

Young chicks are highly susceptible to cold stress. When chilled, they prioritize physical clustering (huddling) over exploring the environment for sustenance, leading to rapid starvation, dehydration, and stunting.

| Parameter | Value |
|---|---|
| **Trigger Condition** | `(sensor.ambient_temp < target.temp - 1.5°C) AND (telemetry.water_intake < target.water_intake × 0.90) AND (batch.age_days ≤ 14)` |
| **Confidence Level** | High (0.88 probability). Confluence of low temperature + simultaneous water intake drop in young birds is definitive chilling signature. |
| **Recommended Action** | ACTUATE → Send MQTT signal to increase gas brooder output by 10%. ALERT → "Critical Chilling Detected. Chicks likely huddling. Verify brooder function and increase heat immediately." |
| **Expected Impact** | Restores thermal comfort, breaks huddling behavior, prompts chicks to resume vital water and feed seeking, mitigating early-stage mortality and irreversible flock stunting. |

### Rule 2: The Heat Stress & Enthalpy Protocol

In the late stages of growth, the massive metabolic heat produced by the birds, combined with high ambient humidity, can push the environment past enthalpy limits where evaporative cooling (panting) remains physically possible.

| Parameter | Value |
|---|---|
| **Trigger Condition** | `(sensor.ambient_temp > target.temp + 2.0°C) AND (sensor.humidity > 65%) AND (telemetry.feed_intake < target.feed_intake × 0.85) AND (telemetry.water_intake > target.water_intake × 1.25)` |
| **Confidence Level** | Very High (0.95 probability). Birds facing lethal heat stress entirely cease eating to eliminate thermic effect of digestion, while massively increasing water intake in desperate cooling attempt. |
| **Recommended Action** | ACTUATE → Ramp all tunnel ventilation fans to 100% capacity (target air exchange >0.70 CFM/bird) and activate evaporative cooling pads. ALERT → "Severe Heat Stress. Enthalpy limits exceeded. Imminent risk of cardiovascular collapse. Maximum cooling engaged." |
| **Expected Impact** | Rapidly extracts latent heat and moisture from housing environment, preventing imminent, flock-wide terminal heart failure. |

### Rule 3: The Pathogenic Outbreak Protocol

Detecting a viral or bacterial outbreak before physical symptoms are noticed by human operators relies on identifying abrupt, simultaneous anomalies across multiple intake and output metrics.

| Parameter | Value |
|---|---|
| **Trigger Condition** | `(log.daily_mortality_rate ≥ 0.5%) OR (telemetry.water_drop ≥ 15ml_per_bird_per_day) AND (telemetry.feed_drop ≥ 8g_per_bird_per_day)` |
| **Confidence Level** | High (0.90 probability). Sudden massive cessation of both feed and water ingestion, perfectly correlated with abnormal mortality spike — classic epidemiological signature of highly virulent diseases (Newcastle Disease, Avian Influenza). |
| **Recommended Action** | ALERT → "CRITICAL BIOSECURITY BREACH. Suspected virulent pathogenic event. Initiate immediate flock isolation. Suspend all personnel movement between houses. Contact state veterinary authority." |
| **Expected Impact** | Halts farm-to-farm and house-to-house disease transmission through immediate quarantine, accelerates timeline for emergency veterinary intervention. |

### Rule 4: The Hypoxia & Ascites Protocol (Altitude Specific)

In high-altitude environments, the sheer speed of modern broiler muscle growth outpaces the capability of the lungs and heart to extract oxygen from the thinner atmosphere, leading to right ventricular hypertrophy, ascites (fluid accumulation in the abdomen), and sudden death.

| Parameter | Value |
|---|---|
| **Trigger Condition** | `(batch.age_days BETWEEN 21 AND 35) AND (log.daily_mortality_rate > 0.25%) AND (telemetry.growth_rate > target.growth_rate × 1.05)` |
| **Confidence Level** | Moderate (0.75 probability). Rapidly growing birds at high altitudes exhibiting mid-to-late stage mortality spikes without corresponding drop in feed intake are almost certainly succumbing to metabolic ascites. |
| **Recommended Action** | ALERT → "High growth trajectory inducing severe hypoxia risk. Implement an immediate 2-hour extension to the dark period lighting schedule to physically slow flock metabolism." |
| **Expected Impact** | Enforcing resting periods reduces the flock's aggregate metabolic oxygen demand, directly curving the incidence of late-stage cardiovascular mortality without requiring pharmaceutical interventions. |

---

## Section 5: Economic Model

An AgriTech system cannot optimize what it cannot financially quantify. The backend architecture must continuously cross-reference biological performance metrics against a real-time ledger of Capital Expenditure (CapEx) and Operational Expenditure (OpEx). The following economic model is structured based on a standard, localized commercial batch (e.g., 500 birds) utilizing contemporary Kenyan Shilling (KES) pricing for the 2025/2026 market horizon.

### 5.1 Cost Matrices (OpEx)

In poultry economics, the cost of nutrition is paramount, routinely constituting 55% to 70% of the total lifecycle production costs.

| Cost Category | Calculation | Total (KES) |
|---|---|---|
| **Chick Cost** | 500 birds × 100 KES (Kenchic hatchery) | 50,000 |
| **Feed Cost** | 5.0 kg per bird × 76 KES/kg (3,800 KES/50kg bag) × 500 birds | 190,000 |
| **Health (Vaccines & Medication)** | 500 birds × 30 KES per bird | 15,000 |
| **Labor & Utilities** | Litter, electricity, heating fuel, general labor — 40 KES per bird × 500 | 20,000 |
| **Total Production Cost** | | **275,000 KES** (550 KES/bird placed) |

### 5.2 Revenue and Yield Projections

| Parameter | Calculation | Value |
|---|---|---|
| **Market Price** | Wholesale live weight (Nairobi/Kenya 2025/2026) | 220–250 KES/kg |
| **Harvest Weight** | Conservative estimate accounting for standard environmental/feed variables | 2.8 kg |
| **Revenue per Bird** | 2.8 kg × 240 KES/kg | 672 KES |
| **Surviving Birds** | 500 × (1 − 0.05 cumulative mortality) | 475 birds |
| **Total Revenue** | 475 × 672 KES | **319,200 KES** |

### 5.3 Profitability and Break-Even Outputs

| Metric | Calculation | Value |
|---|---|---|
| **Gross Profit per Batch** | 319,200 − 275,000 | **44,200 KES** per 500 birds |
| **Net Profit per Bird Placed** | 44,200 ÷ 500 | **~88 KES** |
| **Break-Even Point (Live Weight Price)** | Total Cost ÷ Total Live Biomass = 275,000 ÷ (475 × 2.8 = 1,330 kg) | **206 KES/kg** |

### 5.4 Sensitivity Analysis (Financial Risk Algorithms)

The backend architecture must possess the capability to run continuous Monte Carlo simulations or linear matrix recalculations to project profitability against highly volatile market APIs.

| Economic Scenario | Parameter Input Change | Impact on Net Profit Margin | Recommended KukuFiti System Action |
|---|---|---|---|
| **Feed Price Shock** | Feed costs surge +15% per bag (4,370 KES) due to raw material shortages | Profit drops catastrophically by 64% | Trigger early harvest scenario simulation. Recommend slaughtering at Day 35 instead of Day 42 to eliminate final week of marginal feed inefficiency. |
| **Mortality Spike** | Cumulative mortality increases from baseline 5% to severe 15% | Profit drops by 76% | Isolate biological cause immediately. Recalculate break-even point in real-time. Flag severe financial risk to enterprise stakeholders. |
| **Market Price Collapse** | Wholesale price drops to 210 KES/kg live weight due to seasonal oversupply | Profit approaches 0 (barely clearing break-even) | If current FCR is exceptional, advise holding birds longer to add cheap weight. Alternatively, recommend slaughtering and freezing dressed meat to ride out market glut. |

---

## Section 6: Localization (Africa Focus — Kenya/East Africa)

A generalized agricultural algorithm will fail when applied indiscriminately across varying geographies. The KukuFiti system relies heavily on specific localization metadata to tune its decision engine and thresholds. East Africa, and specifically commercial hubs like Nakuru County in Kenya, presents unique agronomic, climatic, and economic constraints that must be hardcoded into the system's baseline assumptions.

### 6.1 Climatic and Altitude Constraints (The Nakuru Profile)

Nakuru sits in the Great Rift Valley at a high altitude of approximately 1,850 meters (over 6,000 feet). The lower partial pressure of atmospheric oxygen at this altitude exerts a profound physiological impact on fast-growing, heavy broiler strains.

**The Hypoxia Factor:** The reduced availability of atmospheric oxygen forces the bird's heart to pump significantly harder to oxygenate the massive, rapidly growing breast muscle tissue. This sustained cardiovascular pressure inevitably triggers Right Ventricular Hypertrophy, culminating in Ascites syndrome (colloquially known as waterbelly) and sudden death, usually striking between Days 21 and 35.

**Backend System Adjustment:** For farms geolocated in high-altitude zones via the application, the system must automatically adjust the environmental logic to aggressively enforce dark periods (e.g., mandating up to 6 hours of darkness during Weeks 2 and 3) to physically slow the birds' metabolic growth rate, thereby allowing the cardiovascular system sufficient time to catch up to muscle accretion.

### 6.2 Endemic Disease Epidemiology

Disease pressure in East African semi-controlled environments is severe, exacerbated by porous farm biosecurity and the ubiquitous presence of free-ranging backyard flocks (indigenous Kienyeji chickens) that act as continuous vectors for virulent pathogens.

| Disease | Characteristics | Impact |
|---|---|---|
| **Newcastle Disease Virus (NDV)** | Endemic, airborne, highly virulent | 90–100% mortality in unvaccinated broiler flock within days |
| **Infectious Bursal Disease (Gumboro)** | Targets immune system of young chicks by destroying Bursa of Fabricius | Renders flock highly susceptible to secondary bacterial infections; completely blunts subsequent vaccine efficacy |

**Backend System Adjustment (The Vaccination API):** The system must enforce a rigid, localized vaccination protocol by generating push-notification arrays synchronized to the flock's age:

| Day | Vaccine |
|---|---|
| Day 7 | Newcastle (Lasota/HB1 strain) + Infectious Bronchitis via drinking water or ocular drop |
| Day 14 | First crucial dose of Gumboro (IBD) vaccine in drinking water |
| Day 21–24 | Gumboro booster dose |
| Day 28 | Secondary Newcastle booster to secure immunity through finishing phase |

### 6.3 Supply Chain Volatility and Feed Milling Quality

The Kenyan agricultural sector suffers from chronic, structural deficits in raw feed materials, particularly soybeans and maize, leading to high retail prices and highly variable, inconsistent feed quality. Local commercial feed millers (such as Unga Feeds, Pembe, and Permile) are often forced to periodically alter their nutritional formulations based on raw material availability, which can inadvertently shift crucial energy-to-protein ratios.

**Backend System Adjustment:** The KukuFiti system must track the FCR dynamically by individual batch while requiring farmers to log the specific local feed brand utilized. Over time, the backend database will construct a localized regression model mapping specific feed brands against actual biological FCR outcomes. This effectively generates a crowdsourced, empirical quality rating system for local feed millers, allowing farmers to optimize their procurement.

---

## Section 7: Data Model Mapping (Backend-Ready Architecture)

To actualize this comprehensive operational, biological, and economic model, the KukuFiti backend relies on a strictly typed, normalized PostgreSQL database coupled with an asynchronous Python FastAPI routing layer. This architecture ensures high-throughput ingestion of IoT telemetry and rapid execution of the decision engine rules.

### 7.1 Relational Schema (PostgreSQL DDL)

**A. Core Entity Definition Tables**

These tables establish the structural metadata for the application, defining the genetics and the specific operational parameters of a single flock cycle.

```sql
CREATE TABLE breeds (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,         -- e.g., 'Cobb 500', 'Ross 308'
    genetic_fcr_target NUMERIC(4,2)
);

CREATE TABLE batches (
    id SERIAL PRIMARY KEY,
    farm_id INT NOT NULL,
    breed_id INT REFERENCES breeds(id),
    start_date DATE NOT NULL,
    initial_bird_count INT NOT NULL,
    chick_cost_per_bird NUMERIC(10,2) NOT NULL,
    feed_cost_per_kg NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE'    -- 'ACTIVE', 'HARVESTED', 'TERMINATED'
);
```

**B. The Biological Baseline (Target Matrix)**

This table stores the exact 42-day biological targets formulated in Section 2, serving as the immutable ground truth for all anomaly detection algorithms.

```sql
CREATE TABLE batch_targets (
    day_number INT PRIMARY KEY,             -- Day 0 through 42
    expected_weight_g NUMERIC(7,2) NOT NULL,
    expected_daily_feed_g NUMERIC(7,2) NOT NULL,
    expected_cumulative_feed_g NUMERIC(7,2) NOT NULL,
    expected_water_ml NUMERIC(7,2) NOT NULL,
    target_temp_c NUMERIC(4,1) NOT NULL,
    target_rh_pct NUMERIC(4,1) NOT NULL,
    expected_mortality_rate NUMERIC(5,4) NOT NULL
);
```

**C. Daily Telemetry and Logging (Data Ingestion Layer)**

This table functions as a time-series repository, ingesting aggregated sensor data (from hardware) and manual qualitative data (from the farmer app).

```sql
CREATE TABLE daily_logs (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id),
    log_date DATE NOT NULL,
    day_of_cycle INT NOT NULL,              -- Programmatically derived from batch start_date
    actual_temp_avg NUMERIC(4,1),
    actual_rh_avg NUMERIC(4,1),
    feed_consumed_kg NUMERIC(10,2),
    water_consumed_l NUMERIC(10,2),
    mortality_count INT DEFAULT 0,
    cull_count INT DEFAULT 0,
    sample_weight_avg_g NUMERIC(7,2),
    UNIQUE(batch_id, log_date)
);
```

### 7.2 Derived Metrics & Views (Analytical Layer)

To optimize FastAPI endpoint response times and prevent the system from executing computationally heavy aggregations repeatedly on the database server, materialized views are utilized to calculate the complex agricultural KPIs, primarily the real-time Feed Conversion Ratio (FCR) and the compounding mortality matrix.

```sql
CREATE MATERIALIZED VIEW batch_performance_kpis AS
SELECT 
    b.id AS batch_id,
    MAX(dl.day_of_cycle) AS current_age_days,
    SUM(dl.feed_consumed_kg) AS total_feed_consumed_kg,
    SUM(dl.mortality_count + dl.cull_count) AS total_mortality,
    (SUM(dl.mortality_count + dl.cull_count)::DECIMAL / b.initial_bird_count) * 100 
        AS cumulative_mortality_pct,
    (b.initial_bird_count - SUM(dl.mortality_count + dl.cull_count)) 
        AS current_live_bird_count,
    -- FCR Calculation: Total Feed Consumed / Net Live Weight Gained
    CASE 
        WHEN MAX(dl.sample_weight_avg_g) IS NOT NULL THEN 
            (SUM(dl.feed_consumed_kg) * 1000) / 
            ((b.initial_bird_count - SUM(dl.mortality_count)) 
                * (MAX(dl.sample_weight_avg_g) - 42))
        ELSE NULL 
    END AS current_fcr
FROM batches b
JOIN daily_logs dl ON b.id = dl.batch_id
GROUP BY b.id, b.initial_bird_count;
```

### 7.3 API Architecture (FastAPI Endpoint Mapping)

The Python FastAPI backend serves as the nervous system, ingesting MQTT streams from IoT sensor arrays and HTTP POST requests from the mobile application, subsequently triggering the Pydantic-validated logic engine to evaluate the data against the `batch_targets`.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/telemetry/environment` | Ingests high-frequency MQTT payloads from DHT22 temperature and humidity sensors (e.g., every 5 minutes). FastAPI service calculates moving average. If this average deviates significantly from `batch_targets.target_temp_c`, triggers background task to evaluate Rule 1 (Cold Stress) or Rule 2 (Heat Stress), instantly pushing actionable alerts to user or actuating ventilation relays. |
| POST | `/api/v1/logs/daily` | Secure endpoint accepting manual farmer-entered data for end-of-day mortality counts, feed bags utilized, and water meter readings. Triggers refresh of `batch_performance_kpis` materialized view. |
| GET | `/api/v1/analytics/deviations/{batch_id}` | Analytical endpoint comparing accumulated sums in `daily_logs` against expected values in `batch_targets`. If `feed_consumed` deviates by >10% of target over 48-hour window, yields structured JSON alert payload classifying severity of anomaly and projecting resulting financial damage if uncorrected. |
| GET | `/api/v1/financial/projection/{batch_id}` | Enterprise economic dashboard endpoint. Reads `batch_performance_kpis` view, utilizes linear regression to project current FCR trajectory forward to Day 42, applies localized Kenyan market rate variable (e.g., 240 KES/kg), and returns real-time calculated break-even parameter and projected net profit margin. |

By strictly adhering to this architectural, biological, and economic framework, the KukuFiti system transforms from a passive data repository into an active, prescriptive intelligence engine. It ensures the continuous alignment of biological flock welfare, environmental physics, and ultimate commercial profitability, thereby securing sustainable scalability for the agricultural enterprise.

---

# PART II: OPERATIONAL INTELLIGENCE SUPPLEMENT

## Section 8: Pre-Placement Protocol — House Preparation & Commissioning

The single most impactful management intervention in the entire 42-day cycle occurs in the 14 days **before** the first chick arrives. A contaminated, cold, or improperly set-up house will undermine all downstream biological optimization regardless of sensor precision. The KukuFiti system must enforce a structured pre-placement checklist through the application, requiring farm staff to log completion of each step before a new batch can be created in the database.

### 8.1 The 14-Day Cleanout Countdown

The following protocol is sequenced in reverse chronological order from placement day (Day 0). The backend enforces this as a checklist linked to the `batches` table, blocking batch activation unless all critical milestones are logged.

| Days Before Placement | Action | KukuFiti System Trigger |
|---|---|---|
| **Day -14** | Remove all litter, manure, and dead organic material from previous batch. Leave bare concrete floors. | `CLEANOUT_INITIATED` log event created |
| **Day -13** | High-pressure cold water wash of all internal surfaces — walls, ceilings, floors, equipment supports. Remove all feed residue from hoppers. | Manual photo upload + timestamp required |
| **Day -12** | Apply commercial disinfectant spray (e.g., Virocid or Halamid at 1:200 dilution). Maintain 30-minute contact time minimum on all surfaces. | `DISINFECTION_LOGGED` event |
| **Day -11** | 24-hour drying period. Inspect for structural damage: gaps in sidewall curtains, broken fans, cracked concrete (parasite harbourage sites). File maintenance work orders. | Maintenance issue tickets generated in app |
| **Day -10** | Re-spray all surfaces with second disinfectant round (rotation to prevent resistance). Close and seal all entry points for rodent pressure. | `SECOND_DISINFECTION` log |
| **Day -8** | **Formaldehyde Gas Fumigation.** At a rate of 40ml formalin + 20g potassium permanganate per cubic meter of house volume. Seal house for minimum 12 hours. ⚠️ Critical: No personnel inside during fumigation. PPE mandatory during setup. | App issues fumigation timer; 12-hour lockout enforced |
| **Day -7** | Open and ventilate house for 24 hours. Conduct final inspection: clean, dry, and no odour of ammonia or formalin. | `FUMIGATION_CLEARED` event |
| **Day -5** | Install fresh litter material. Target depth: **50mm (5cm)** wood shavings for Phase 1. Distribute evenly. In humid seasons (March–June), apply a litter treatment such as PLT (Poultry Litter Treatment) at 50g/m² to pre-neutralize ammonia-generating bacteria. | Litter depth and material brand logged |
| **Day -4** | Install and test all equipment: brooder gas lines, nipple drinker lines (pressure test at 20 kPa), feed hopper mechanisms, fans (test each fan individually for correct rotation direction), and temperature/humidity sensors. | Equipment test matrix checklist — all items must be `PASS` |
| **Day -3** | Connect temperature and humidity sensors to KukuFiti backend. Initiate pre-heating. Begin warming house to **32°C at chick level** using gas brooders. | System auto-activates `PRE_HEATING` stage for pending batch |
| **Day -2** | Fill all water lines. Flush with chlorinated water (3–5 ppm free chlorine). Verify drinker height is set at chick-back level. Calibrate and test all gas sensors (NH3, CO2). Place paper feed mats on litter surface. | Water quality log: pH (6.0–7.0), chlorine (3–5 ppm) |
| **Day -1** | Final thermal soak: confirm house has held ≥32°C for minimum 12 consecutive hours at chick level (not ceiling level). Humidity at 60–70%. System confirms sensor baseline before chick arrival is authorized. | `HOUSE_READY` status unlocks batch activation in app |
| **Day 0** | Chick arrival. Place immediately under brooders. Log: hatchery source, transport vehicle ID, chick supplier batch number, hatch date, and first-hour mortality count (culls at placement). | `BATCH_ACTIVATED` — all monitoring and baseline comparison initiates |

### 8.2 Litter Material Selection Matrix

The choice of litter material has direct implications for ammonia generation, footpad health, and disease pressure — all critical in the Kenyan context where wood shavings quality is variable.

| Material | Absorbency | Ammonia Risk | Availability (Kenya) | Recommended? |
|---|---|---|---|---|
| **Wood shavings (softwood)** | High | Low | High (sawmills, Nakuru/Eldoret) | ✅ Primary choice |
| Rice husks | Medium | Medium | Seasonal (Mwea region) | ✅ Secondary |
| Sugarcane bagasse | Low-Medium | High | Western Kenya | ⚠️ Acceptable with PLT treatment |
| Sawdust (fine) | Very High | Very High | High | ❌ Avoid — packs, anaerobic layer forms |
| Newspaper/cardboard | Low | Very High | Not scalable | ❌ For starter paper only |

**Depth Protocol by Phase:**

| Phase | Depth | Notes |
|---|---|---|
| **Phase 1 (Day 0–7)** | 50mm (5cm) | Sufficient depth for thermal insulation, critical for chick comfort |
| **Phase 2 (Day 8–14)** | No additional | Unless compaction detected |
| **Phase 3 (Day 15–28)** | Add 20mm top-dress | If moisture exceeds 30% (litter moisture sensor threshold) |
| **Phase 4 (Day 29–42)** | Add 20mm top-dress | In high-traffic areas near feeders and drinkers |

**Backend Schema Addition:**

```sql
CREATE TABLE pre_placement_checklist (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id),
    check_date DATE NOT NULL,
    days_before_placement INT NOT NULL,
    task_code VARCHAR(50) NOT NULL,         -- 'DISINFECTION_1', 'FUMIGATION', 'SENSOR_TEST'
    completed BOOLEAN DEFAULT FALSE,
    completed_by VARCHAR(100),
    notes TEXT,
    photo_url TEXT,                          -- S3/Cloudinary reference
    UNIQUE(batch_id, task_code)
);

CREATE VIEW batch_readiness AS
SELECT 
    b.id AS batch_id,
    b.status,
    COUNT(p.id) FILTER (WHERE p.completed = TRUE) AS completed_tasks,
    COUNT(p.id) AS total_tasks,
    BOOL_AND(p.completed) AS house_ready
FROM batches b
LEFT JOIN pre_placement_checklist p ON b.id = p.batch_id
GROUP BY b.id, b.status;
```

---

## Section 9: Water Quality & Sanitation Management

Water is the single most under-managed resource in East African commercial broiler production. The industry routinely focuses on quantity (nipple flow rates) while neglecting quality — a critical oversight given that broilers consume nearly twice as much water as feed by weight, making contaminated water lines a direct vector for disease amplification throughout an entire flock.

### 9.1 Water Quality Parameters

The KukuFiti system must accept water quality test results as manual inputs at minimum once per week, flagging any parameter that falls outside the safe biological window.

| Parameter | Acceptable Range | Warning Threshold | Critical Threshold | Biological Consequence |
|---|---|---|---|---|
| **pH** | 6.0 – 7.0 | <5.5 or >8.0 | <5.0 or >8.5 | Outside range: medication/vaccine efficacy drops >40%; mineral precipitation blocks nipples |
| **Free Chlorine (residual)** | 0.5 – 3.0 ppm | >3.5 ppm | >5.0 ppm | High chlorine: inactivates live vaccines, kills beneficial gut bacteria |
| **Total Dissolved Solids (TDS)** | <1,000 mg/L | 1,000–2,000 mg/L | >2,000 mg/L | High TDS: electrolyte imbalance, diarrhea, increased Phase 1 mortality |
| **Total Bacterial Count** | <100 CFU/ml | 100–1,000 CFU/ml | >1,000 CFU/ml | Enteric disease, necrotic enteritis, high Phase 1 mortality |
| **Water Temperature (line)** | 10°C – 21°C | >25°C | >30°C | >30°C: birds refuse to drink → cascading feed intake collapse |
| **Nitrates** | <10 mg/L | 10–50 mg/L | >50 mg/L | Methaemoglobinaemia (blood oxygen blockage) in young chicks |
| **Sulphates** | <200 mg/L | 200–500 mg/L | >500 mg/L | Laxative effect, wet litter, coccidiosis vector |

### 9.2 Water Line Sanitation Protocol

Biofilm is the primary water-line threat. A biofilm layer of only 50 microns on the interior of water pipes can harbour pathogen loads 1,000× higher than the surrounding water column, and it renders chlorination ineffective at standard doses.

**Phase-Based Chlorination Schedule:**

| Phase | Chlorine Dose (ppm in header tank) | Notes |
|---|---|---|
| Pre-placement | 50–100 ppm shock dose, 2-hour contact | Full line flush before chick arrival |
| Day 0–7 (Brooding) | 1.0–2.0 ppm residual | Low dose — avoid vaccine inactivation. Never chlorinate ≤4 hours before/after vaccine dosing. |
| Day 8–28 | 2.0–3.0 ppm residual | Increasing bacterial pressure as flock age and litter moisture rise |
| Day 29–42 | 3.0–5.0 ppm OR hydrogen peroxide 35% at 1L/1000L | H2O2 alternative strips biofilm more aggressively in finishing phase |
| Post-harvest / Cleanout | 100–200 ppm shock + overnight soak | Full line sterilization before house cleanout begins |

**Weekly Line Flush Protocol (Backend-triggered reminder):**
Every 7 days, the system must prompt the farm manager to:
1. Remove end-cap from the terminal nipple line
2. Open water at maximum pressure for 60 seconds per line section
3. Inspect drained water — if turbid or discoloured, escalate to full line acidification treatment
4. Replace end-cap, re-pressurize to 20 kPa for Phase 1, scaling to 35–45 kPa for Phase 3–4

**Acidification (Organic Acid Treatment):**
When biofilm is suspected (confirmed by declining water intake without temperature explanation), flush lines with a citric acid or formic acid solution (e.g., Aqua-Acid at 1–2 ml/L) for a 4-hour soak. This drops water pH to ~4.0–4.5, dissolving mineral scale and stripping biofilm matrix. Follow immediately with a clean water flush before birds resume drinking.

```sql
CREATE TABLE water_quality_logs (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id),
    log_date DATE NOT NULL,
    day_of_cycle INT NOT NULL,
    ph NUMERIC(4,2),
    free_chlorine_ppm NUMERIC(5,2),
    tds_mg_l NUMERIC(7,1),
    water_temp_c NUMERIC(4,1),
    nitrates_mg_l NUMERIC(6,1),
    bacterial_count_cfu_ml INT,
    treatment_applied VARCHAR(100),         -- 'CHLORINATION_3PPM', 'H2O2_FLUSH', 'ACID_TREATMENT'
    sampled_from VARCHAR(50),               -- 'HEADER_TANK', 'MID_LINE', 'TERMINAL_NIPPLE'
    flag_status VARCHAR(20) DEFAULT 'OK',   -- 'OK', 'WARNING', 'CRITICAL'
    UNIQUE(batch_id, log_date, sampled_from)
);
```

---

## Section 10: Litter Management Science

Litter quality is the most underestimated determinant of flock profitability in East African broiler production. Poor litter management is the primary driver of pododermatitis (footpad lesions), hock burns, breast blisters, coccidiosis outbreaks, and excessive ammonia — all of which directly depress feed conversion efficiency and condemn carcasses at slaughter.

### 10.1 Litter Moisture Science

**Target Moisture Range: 25–35%**

Litter below 20% moisture becomes dusty — a respiratory irritant and vector for airborne pathogens. Litter above 40% moisture becomes wet and anaerobic, generating ammonia at an accelerating rate while providing the warm, moist environment required for *Eimeria* (coccidiosis) oocyst sporulation.

**Field Moisture Estimation (no laboratory):** The squeeze test is the standard field protocol. Take a handful of litter, compress tightly in the fist, then release:
- Litter falls apart immediately → **<20% moisture** (too dry)
- Litter holds shape briefly then slowly crumbles → **25–35%** (target)
- Litter holds solid shape and feels wet → **>40%** (danger zone)
- Water drips from litter → **>60%** (critical — immediate intervention)

**Ammonia Generation Model:**

The backend must implement the following ammonia risk model, triggered when both moisture AND temperature readings are available:

```
Ammonia Risk Score = (litter_moisture_pct - 25) × 0.4 + (ambient_temp_c - 20) × 0.6
```

| Ammonia Risk Score | NH3 Estimate (ppm) | System Response |
|---|---|---|
| < 0 | < 5 ppm | ✅ Normal |
| 0 – 5 | 5–15 ppm | ⚠️ WARN: "Increase ventilation rate by 15%" |
| 5 – 10 | 15–25 ppm | ⚠️ HIGH: "Apply PLT treatment. Increase ventilation. Check drinker leaks." |
| > 10 | > 25 ppm | 🚨 CRITICAL: "Ammonia approaching lethal threshold. Immediate partial litter removal required." |

**The Ammonia Thresholds:**
- > 10 ppm: Measurable reduction in mucociliary clearance (respiratory defense)
- > 25 ppm: Confirmed damage to respiratory epithelium, severe immunosuppression
- > 50 ppm: Corneal ulceration (birds close eyes), severe mortality spike, FCR collapse

### 10.2 Litter Caking: Detection & Remediation

Litter caking (surface crusting over a wet anaerobic underlayer) is endemic in Kenyan poultry houses during long rains season (March–May) and short rains (October–December). The caked surface creates a physical barrier preventing ammonia gas escape, concentrating it at bird level.

**Caking Detection Protocol:**
- Visual: Surface appears dry and solid but breaks away in chunks revealing wet dark material underneath
- Olfactory: Strong ammonia odour despite apparent surface dryness

**Remediation Sequence:**
1. **Mechanical disruption:** Break and turn caked areas with a garden fork to depths of 30–40mm. This must be performed when birds are at the opposite end of the house.
2. **Drying agent application:** Apply hydrated lime (calcium hydroxide) at 0.5 kg/m² over the disturbed area. Allow 4 hours before birds return to the area. Lime raises pH to >12, killing coccidiosis oocysts and suppressing ammonia-producing bacteria.
3. **Increase ventilation:** Ramp fans to maximum for 2–4 hours post-treatment.
4. **Top-dress if necessary:** If moisture cannot be reduced, apply 20mm fresh litter over the affected area.

⚠️ **Critical Kenya Note:** Never apply lime during Phase 1 (Day 0–7). Young chicks will ingest lime particles, causing severe crop impaction. Lime is safe from Day 10 onwards.

```sql
CREATE TABLE litter_assessments (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id),
    assessment_date DATE NOT NULL,
    day_of_cycle INT NOT NULL,
    moisture_estimate_pct NUMERIC(4,1),
    caking_present BOOLEAN DEFAULT FALSE,
    caking_area_pct NUMERIC(4,1),
    treatment_applied VARCHAR(100),
    lime_kg_applied NUMERIC(6,2),
    ammonia_risk_score NUMERIC(5,2),        -- Computed by backend
    footpad_score_avg NUMERIC(3,1),         -- 0=clean, 1=mild, 2=severe lesions (sample of 10 birds)
    notes TEXT
);
```

---

## Section 11: Advanced Lighting Science

The lighting program in commercial broiler production directly controls the bird's feeding behaviour, metabolic rate, cardiovascular development, and immune function. It is simultaneously the most cost-effective and most misunderstood management tool available to the farm operator.

### 11.1 The KukuFiti Standard Broiler Lighting Program

The following program is the recommended baseline for Kenyan farms, balancing feed intake optimization against cardiovascular protection at altitude:

| Phase | Days | Light Period | Dark Period | Intensity (Lux at bird level) | Rationale |
|---|---|---|---|---|---|
| Stimulation | 0–2 | 24 hours | 0 hours | 20–40 lux | 100% light ensures all chicks locate feed and water before yolk reserves deplete (~48h post-hatch) |
| Circadian Establishment | 3–7 | 23 hours | 1 hour (split into 2× 30-min) | 15–20 lux | Minimum dark required for melatonin rhythm; multiple short dark periods are less stressful than one |
| Growth Optimization | 8–14 | 20 hours | 4 hours (continuous) | 10–15 lux | Forced rest period slows early growth rate, protecting cardiovascular development at altitude |
| Controlled Growth | 15–21 | 18 hours | 6 hours (continuous) | 8–10 lux | 6 hours of darkness at the altitude-risk peak window (Nakuru: 1,850m) is the primary hypoxia/ascites prevention tool |
| Growth Acceleration | 22–35 | 20 hours | 4 hours | 5–10 lux | Restored light for maximum feed intake during muscle hypertrophy phase |
| Pre-Harvest Feed Push | 36–42 | 22–23 hours | 1–2 hours | 5 lux minimum | Maximum feed intake to push final harvest weight; lights never 100% off (prevents panic and pile-ups) |

**⚠️ Critical Rule:** Broilers must **never** experience complete darkness (0 lux) after Day 3. Complete darkness triggers flock panic — birds pile into corners and suffocate each other. Maintain a minimum of 0.5 lux even during "dark" periods.

### 11.2 Lux Level Implementation

| Lux Level | Practical Equivalent | Cost Implementation |
|---|---|---|
| 40+ lux | Brightly lit office | For Day 0–2 stimulation only |
| 20 lux | Comfortable reading light | Standard LED tubes at 2m spacing |
| 10 lux | Dimly lit corridor | Dimmers at 50% or reduced density |
| 5 lux | Twilight outdoors | Dimmers at 25%, energy efficient |
| 0.5 lux (safety minimum) | Moonlight | Single 5W LED per 100m² as nightlight |

**Kenya Implementation Note:** Natural daylight in Kenya is approximately 12 hours (we sit close to the equator — sunrise ~6:15am, sunset ~6:45pm year-round). This means the lighting program must actively compensate for daylight ingress through sidewall curtains. **Blackout housing is the gold standard.** For non-blackout houses, the KukuFiti system must import sunrise/sunset data for the farm's GPS coordinates and alert the farm manager when natural light duration conflicts with the programmed dark periods.

```sql
CREATE TABLE lighting_programs (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id),
    day_number INT NOT NULL,
    target_light_hours NUMERIC(4,1) NOT NULL,
    target_dark_hours NUMERIC(4,1) NOT NULL,
    target_lux_min NUMERIC(6,1),
    target_lux_max NUMERIC(6,1),
    dark_period_start TIME,
    dark_period_end TIME,
    split_dark BOOLEAN DEFAULT FALSE,
    UNIQUE(batch_id, day_number)
);

CREATE TABLE lighting_actuations (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id),
    actuation_timestamp TIMESTAMPTZ NOT NULL,
    action VARCHAR(20) NOT NULL,            -- 'LIGHTS_ON', 'LIGHTS_OFF', 'DIM_50', 'DIM_25'
    triggered_by VARCHAR(30) NOT NULL,      -- 'SCHEDULE', 'MANUAL_OVERRIDE', 'EMERGENCY'
    lux_sensor_reading NUMERIC(6,1)
);
```

---

## Section 12: Flock Uniformity & Statistical Sampling

A highly uniform flock — where the majority of birds are within a narrow weight band — is far more manageable than a bipolar flock with a broad weight distribution. Uniformity determines the accuracy of the daily log's `sample_weight_avg_g` value and therefore the precision of every downstream calculation in the KukuFiti system.

### 12.1 Coefficient of Variation (CV) — The Uniformity Metric

**Uniformity is expressed as the Coefficient of Variation (CV):**

```
CV (%) = (Standard Deviation of Sample Weights / Mean Sample Weight) × 100
```

| CV Score | Uniformity Grade | Interpretation | KukuFiti Action |
|---|---|---|---|
| < 8% | Excellent | Tight flock — predictable performance | ✅ No action |
| 8–12% | Good | Acceptable spread | Monitor weekly |
| 12–15% | Moderate | Early detection of feed competition or health problems | ⚠️ WARN: Review feeder space allocation |
| 15–20% | Poor | Significant runts developing, bimodal weight distribution | 🚨 ALERT: Separate lightweight birds if possible |
| > 20% | Critical | Flock salvage situation | 🚨 CRITICAL: Immediate veterinary and nutritional review |

**Target CV for Cobb 500 / Ross 308 flocks:** ≤ 10% at Day 21; ≤ 12% at Day 35.

### 12.2 Sampling Protocol

**Sample Size Calculation:**
For statistically valid weight data (95% confidence, ±3% margin of error), the minimum sample is:

```
n = (Z² × σ²) / E²

Where: Z = 1.96 (95% CI), σ = estimated CV×mean, E = acceptable error (3% of mean)
For a 500-bird flock at Day 21 (mean ~1,116g, CV 10%): n ≈ 43 birds
```

**Practical Rule:** Sample minimum **3% of the flock** or **50 birds**, whichever is larger. For a 500-bird house: sample 50 birds (10%). For a 5,000-bird house: sample 150 birds (3%).

**Sampling Frequency:**

| Day | Purpose |
|---|---|
| Day 7 | First official weight check (validate brooding phase performance) |
| Day 14 | Phase 2 exit validation |
| Day 21 | **Critical check** — mid-growth uniformity assessment, ascites risk window |
| Day 28 | Phase 3 exit, FCR projection update |
| Day 35 | Pre-harvest assessment and early slaughter decision trigger |
| Day 42 | Final harvest weight |

**Sampling Methodology:** Blind random catch using a catching frame. Weigh individually on calibrated spring or digital scale. Never selectively catch the largest or most accessible birds — this introduces severe positive bias.

```sql
CREATE TABLE weight_samples (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id),
    sample_date DATE NOT NULL,
    day_of_cycle INT NOT NULL,
    birds_sampled INT NOT NULL,
    mean_weight_g NUMERIC(7,2) NOT NULL,
    std_deviation_g NUMERIC(7,2),
    cv_pct NUMERIC(5,2),
    min_weight_g NUMERIC(7,2),
    max_weight_g NUMERIC(7,2),
    weight_at_target_pct NUMERIC(5,2),
    uniformity_grade VARCHAR(15),           -- 'EXCELLENT', 'GOOD', 'MODERATE', 'POOR', 'CRITICAL'
    sampler_name VARCHAR(100)
);
```

---

## Section 13: Stocking Density & Thinning Management

Stocking density is the primary physical constraint on the thermal environment in Phase 3 and 4. As birds grow, their combined metabolic heat output and moisture production per square meter increases dramatically, creating a positive feedback loop between bird density, ambient temperature, and mortality risk.

### 13.1 Density Calculations

**Industry Standard Limits for East Africa:**

| Metric | Recommended Maximum | Upper Absolute Limit | Note |
|---|---|---|---|
| Birds per m² | 30–33 birds/m² (at placement) | 38 birds/m² | Higher density requires mechanized ventilation |
| kg live weight/m² | 30–33 kg/m² (at harvest) | 39 kg/m² | The binding constraint in Phase 4 |

**Example Calculation for a 10m × 15m house (150m²):**
- At placement (42g/bird): 33 birds/m² × 150m² = **4,950 birds** at 207 kg total biomass
- At Day 42 (3.27kg/bird, 5% mortality): 4,702 live birds × 3.27kg = **15,375 kg** = **102.5 kg/m²**
- This is 3× the safe limit → thinning is **mandatory** starting Day 35

### 13.2 Thinning Schedule

Thinning (partial harvest) removes a portion of the flock early to reduce density for the remaining birds, allowing the survivors to reach maximum live weight without heat stress.

| Thinning Event | Timing | % of Flock Removed | Trigger Condition |
|---|---|---|---|
| **Thin 1** | Day 35 | 25–30% of remaining flock | Biomass approaching 25 kg/m²; buyer order confirmed |
| **Thin 2** | Day 38 | 25% of remaining flock | Post-thin density check confirms >20 kg/m² still |
| **Final Harvest** | Day 41–42 | 100% of remaining birds | All birds cleared |

**Post-Thin Environmental Recalibration:**
After each thinning, the KukuFiti backend must recalculate environmental parameters for the reduced flock:
- Reduce ventilation by 20–25% for first 24 hours (reduced heat load)
- Adjust brooder set-points if thinning occurs in cool weather
- Recalculate daily feed and water targets for the new bird count

```sql
ALTER TABLE batches ADD COLUMN thinning_events JSONB DEFAULT '[]';
-- JSONB structure: [{"date": "2025-03-15", "day": 35, "birds_removed": 1250, "avg_weight_g": 2510, "price_kes": 240}]

CREATE TABLE thinning_events (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id),
    event_date DATE NOT NULL,
    day_of_cycle INT NOT NULL,
    birds_removed INT NOT NULL,
    avg_live_weight_g NUMERIC(7,2),
    market_price_kes_per_kg NUMERIC(8,2),
    buyer_name VARCHAR(100),
    revenue_kes NUMERIC(12,2),
    remaining_birds INT NOT NULL,
    new_density_kg_m2 NUMERIC(6,2)
);
```

---

## Section 14: Biosecurity Standard Operating Procedures

Biosecurity is the totality of measures that prevent pathogenic agents from entering, spreading within, or exiting a poultry operation. In the Kenyan context — where commercial broiler houses frequently co-exist within 500 metres of free-range Kienyeji flocks that carry endemic Newcastle Disease Virus (NDV), Marek's Disease, and Infectious Bronchitis — a formal biosecurity SOP is not optional; it is the primary line of defense against catastrophic flock loss.

### 14.1 The Three Biosecurity Zones

Every KukuFiti farm is modelled as a three-zone security architecture:

**Zone 1 — Clean Zone (Inside the poultry house):**
- Access requires full PPE: dedicated boots (footbath dipped), coveralls, hairnet
- No personal mobile phones unless in a sealed bag
- No food, drink, or tobacco
- Entry log mandatory in KukuFiti app (timestamp, name, purpose)

**Zone 2 — Controlled Zone (Farm perimeter, 10m around house):**
- Visitors may enter with foot dip compliance and visitor log entry
- No poultry or egg products from external sources allowed
- All vehicles must be stopped and wheel arches/undersides sprayed with disinfectant

**Zone 3 — Public Zone (Farm road, loading areas):**
- Buyers, feed delivery trucks, and catch crews operate in Zone 3 only
- Live bird crates must be new or fumigated before entering Zone 3
- No Zone 3 personnel may enter Zone 2 without zone transition protocol

### 14.2 Footbath Protocol

Footbaths are the most critical and most mismanaged biosecurity tool in Kenyan poultry.

| Parameter | Requirement | Common Kenya Failure Mode |
|---|---|---|
| **Disinfectant** | Quaternary ammonium compound (e.g., Trigene) OR Halamid (1–2%) | Using water only; expired product |
| **Concentration** | As per manufacturer specification (check with test strips) | Dilution not measured |
| **Contact time** | Minimum 30 seconds per boot | Cursory step-through |
| **Change frequency** | Every 24 hours, or immediately when visibly contaminated | Changed weekly or never |
| **Depth** | Minimum 50mm liquid depth | Shallow tray dries out |
| **Boot scraping** | All mud and organic material removed with brush BEFORE footbath | Organic matter inactivates disinfectant |

**KukuFiti App Enforcement:** The system generates a daily footbath maintenance reminder at 06:00. The farm manager must log footbath change as confirmed or snoozed. Three consecutive snoozes trigger an alert to the farm owner.

### 14.3 Visitor & Vehicle Log

```sql
CREATE TABLE biosecurity_log (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id),
    log_timestamp TIMESTAMPTZ NOT NULL,
    entry_type VARCHAR(20) NOT NULL,        -- 'PERSON', 'VEHICLE', 'EQUIPMENT'
    visitor_name VARCHAR(100),
    visitor_role VARCHAR(50),               -- 'VET', 'FEED_DELIVERY', 'BUYER', 'FARM_STAFF', 'OWNER'
    zone_accessed INT NOT NULL,             -- 1, 2, or 3
    ppe_confirmed BOOLEAN DEFAULT FALSE,
    footbath_confirmed BOOLEAN DEFAULT FALSE,
    purpose TEXT,
    last_poultry_contact_days INT,
    approved_by VARCHAR(100)
);

-- Rule: If visitor_role = 'BUYER' or last_poultry_contact_days < 3, zone_accessed must be 3 only
```

---

## Section 15: Disease Identification Matrix & Treatment Protocols

The following matrix is the clinical decision support tool for the KukuFiti system's alert engine. When a farm manager inputs qualitative observations into the daily log, the backend cross-references the symptom pattern against this matrix and generates a ranked list of probable diagnoses with recommended immediate actions. This is not a replacement for veterinary consultation — it is a rapid triage tool to minimize the time between symptom onset and intervention.

### 15.1 Disease Symptom → Diagnosis → Treatment Matrix

| Disease | Peak Risk Days | Primary Symptoms | Post-Mortem Findings | Vaccine (Kenya Brand) | Treatment |
|---|---|---|---|---|---|
| **Newcastle Disease (NDV)** | Any age | Sudden onset; respiratory gasping, twisted necks (torticollis), green diarrhoea, mortality 50–100% in unvaccinated flocks | Haemorrhagic lesions in intestinal tract, necrotic tonsils | Kenchic NDV (Lasota) — Day 7 and Day 28 | No treatment. Emergency vaccination of remaining birds if <50% affected. Notify state veterinary. |
| **Gumboro (IBD)** | Day 14–28 | Sudden depression, ruffled feathers, watery white diarrhoea, birds pecking at own vents, staggering | Bursa of Fabricius enlarged and haemorrhagic (cherry-red), thigh muscle haemorrhage | Hipragumboro or Bursine-2 — Day 14, booster Day 21 | Electrolyte supplementation (ORS in water). Vitamin C at 200g/1000L. Antibiotic for secondary infections. Supportive care only. |
| **Coccidiosis (Eimeria)** | Day 14–35 | Bloody or coffee-coloured diarrhoea, hunched birds, reduced feed intake, wet litter | Intestinal haemorrhage, petechiae on intestinal wall | Prevention: Amprolium in feed (coccidiostat), NOT a live vaccine | **Diclazuril** (Clinacox) or **Toltrazuril** (Baycox) at 1ml/L water for 2 consecutive days. PLT + lime on litter immediately. |
| **Infectious Bronchitis (IB)** | Any age | Sneezing, tracheal rales (rattling breath), watery eyes, drop in feed intake | Mucus in trachea, air sacculitis | IB H120 vaccine (Day 7 combined with NDV) | Antibiotics for secondary *E. coli* pneumonia. Vitamin A at 500,000 IU/1000L for mucosa recovery. |
| **Chronic Respiratory Disease (CRD/Mycoplasmosis)** | Day 15–40 | Slow-onset respiratory rattle, facial swelling, clear nasal discharge, gradual FCR decline | Air sac inflammation ("air sac disease"), frosted glass appearance | Not vaccinated commercially in Kenya | **Tylosin** (Tylan) at 500mg/L water for 5 days OR **Enrofloxacin** for acute cases. Note: enrofloxacin has withdrawal period. |
| **Necrotic Enteritis (NE)** | Day 14–35 | Sudden increased mortality (1–2% per day), birds found dead without warning, reddish diarrhoea | Friable, gas-filled intestines with dark necrotic plaques | None — controlled by coccidiosis prevention and balanced gut flora | **Amoxicillin** or **Penicillin** in water for 5 days. Review coccidiostat program. |
| **Marek's Disease** | Day 21+ | Progressive leg paralysis, wing droop, grey iris, weight loss in individual birds over weeks | Tumours on peripheral nerves, liver, spleen | Kenchic Marek's vaccine — administered at hatchery Day 0 (not farm-level) | No treatment. Cull affected birds immediately. Ensure hatchery vaccination confirmed on delivery certificates. |
| **Ascites (Waterbelly)** | Day 21–40 | Distended abdomen, blue/purple comb, reluctance to move, birds found dead on backs | Fluid in body cavity, enlarged right ventricle, pale liver | Not a pathogen — metabolic/hypoxia. Prevent via dark period management. | Extend dark period by 1 hour immediately. Reduce feed access for 2 hours/day. Vitamin C + E supplementation. Cull affected birds. |
| **Heat Stress Collapse** | Day 21–42 | Panting, wings spread, birds at water points, cessation of eating, rapid mass mortality in severe cases | No specific lesions — congestion, pulmonary oedema | Not a pathogen — environmental. Prevent via ventilation. | Emergency: maximize ventilation, activate fogging/evaporative cooling, add electrolytes (sodium bicarbonate + potassium chloride) to water. |

### 15.2 Vaccination Schedule (Kenya-Localized)

The KukuFiti app must auto-generate push notification reminders for each vaccination event based on the batch's `start_date`. All vaccination events must be logged with the brand, batch number, dose, and administration method.

| Day | Vaccine | Disease | Route | Dose | Brand (Kenya) | Critical Notes |
|---|---|---|---|---|---|---|
| 0 (Hatchery) | Marek's HVT | Marek's Disease | SC injection | 1 dose/bird | Kenchic / Prime Hatch | Confirm on delivery certificate — not farm-administered |
| 7 | NDV + IB (combined) | Newcastle + Bronchitis | Drinking water or eye drop | 1 dose/bird | Hipraviar-S OR CEVAC IBird | Do NOT chlorinate water 4 hours before/after. Use skimmed milk as stabilizer (2.5g/L) |
| 14 | Gumboro (IBD) — Dose 1 | Infectious Bursal Disease | Drinking water | 1 dose/bird | Hipragumboro OR Bursine-2 | Withhold water for 1 hour pre-vaccination to ensure all birds drink actively |
| 21 | Gumboro (IBD) — Dose 2 (Booster) | Infectious Bursal Disease | Drinking water | 1 dose/bird | Same brand as Dose 1 | Do not mix brands between Dose 1 and Dose 2 |
| 28 | NDV — Booster | Newcastle Disease | Drinking water | 1 dose/bird | Kenchic NDV Lasota | Critical: protects through the finishing phase into slaughter |

```sql
CREATE TABLE vaccination_events (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id),
    scheduled_date DATE NOT NULL,
    day_of_cycle INT NOT NULL,
    vaccine_name VARCHAR(100) NOT NULL,
    disease_target VARCHAR(100) NOT NULL,
    route VARCHAR(30) NOT NULL,             -- 'DRINKING_WATER', 'EYE_DROP', 'SPRAY', 'INJECTION'
    brand VARCHAR(100),
    vaccine_batch_number VARCHAR(100),
    dose_per_bird NUMERIC(6,3),
    birds_vaccinated INT,
    completed BOOLEAN DEFAULT FALSE,
    completed_by VARCHAR(100),
    completion_timestamp TIMESTAMPTZ,
    water_chlorine_suspended BOOLEAN,
    stabilizer_used VARCHAR(50),            -- 'SKIMMED_MILK_2.5G_L'
    cold_chain_confirmed BOOLEAN DEFAULT FALSE,
    notes TEXT
);
```

---

## Section 16: Kenya Seasonal Calendar Integration

Kenya's equatorial position creates two annual rainfall seasons that profoundly alter the thermal and humidity environment inside every poultry house in the country. Ignoring the seasonal calendar is the single most common cause of flock losses in Kenyan commercial broiler production. The KukuFiti backend must integrate seasonal awareness into its threshold models, automatically adjusting warning levels and recommended interventions based on the calendar date and the farm's GPS-derived climate zone.

### 16.1 Kenya Annual Poultry Farming Calendar

| Season | Months | Conditions | Primary Risk | KukuFiti System Adjustment |
|---|---|---|---|---|
| **Long Rains** | March – May | High humidity (75–90%), cool temps (16–22°C in Nakuru), persistent cloud cover | Litter moisture, coccidiosis, fungal feed spoilage | Lower litter moisture thresholds to trigger warnings at >30%; increase ventilation targets by 15%; alert feed storage moisture monitoring |
| **Cool Dry Season** | June – August | Low humidity (40–55%), cold nights (8–14°C in Nakuru), strong SE trade winds | Cold stress in Phase 1, high ammonia from dry litter at low temperatures, increased fuel cost for brooding | Increase Phase 1 target temperature by 1°C; activate cold stress alerts at lower deviation thresholds; increase brooding fuel budget estimate |
| **Short Rains** | October – December | Moderate humidity (60–75%), warm days (20–26°C), unpredictable rainfall | Litter moisture, sudden temperature spikes, coccidiosis if litter management lapses | Mirror long rains adjustments at 80% intensity; flag unpredictable temperature variance |
| **Hot Dry Season** | January – February | Low humidity (30–45%), high daytime temps (26–32°C in Nakuru), intense solar radiation | Heat stress in Phase 3–4, accelerated water consumption, enthalpy risk | Reduce Phase 4 upper temperature threshold by 1°C (trigger heat stress alerts sooner); increase water target calculations by 20%; flag roof insulation adequacy |

### 16.2 Optimal Batch Start Scheduling

The KukuFiti system must provide a **Batch Start Planner** that helps farm managers choose start dates that align Phase 3 and 4 (the highest-risk, heat-sensitive phases, Day 15–42) with cooler seasonal windows.

**Target Alignment: Phase 3–4 during Cool Dry Season (June–August)**

| Start Month | Phase 3 Occurs In | Phase 4 Occurs In | Risk Rating | Recommendation |
|---|---|---|---|---|
| January | March (Long Rains) | March–April | 🔴 HIGH | Avoid — peak humidity during most critical phase |
| February | April (Long Rains peak) | April–May | 🔴 HIGH | Avoid |
| March | May (Rains easing) | May–June | 🟡 MODERATE | Acceptable with enhanced ventilation |
| April | June (Cool Dry) | June–July | 🟢 LOW | **Optimal** — finishing phase in coolest, driest months |
| May | July (Cool Dry) | July–August | 🟢 LOW | **Optimal** |
| June | August (Cool Dry) | August–Sept | 🟢 LOW | **Optimal** |
| July | September (Transitional) | September–Oct | 🟡 MODERATE | Acceptable |
| August | October (Short Rains begin) | Oct–Nov | 🟡 MODERATE | Monitor humidity closely |
| September | November (Short Rains) | Nov–Dec | 🟡 MODERATE | Enhanced litter management required |
| October | December (Short Rains) | Dec–Jan | 🔴 HIGH | High risk — festive demand drives prices up, offsetting risk |
| November | January (Hot Dry) | Jan–Feb | 🔴 HIGH | Avoid unless cooling infrastructure is excellent |
| December | February (Hot Dry) | Feb–March | 🟡 MODERATE | Acceptable for experienced farms only |

```sql
CREATE TABLE farm_location (
    id SERIAL PRIMARY KEY,
    farm_id INT NOT NULL,
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    altitude_m NUMERIC(7,1),
    climate_zone VARCHAR(50),              -- 'HIGHLAND', 'MIDLAND', 'LOWLAND'
    nakuru_profile BOOLEAN DEFAULT FALSE,  -- Enables altitude-specific adjustments
    avg_temp_by_month JSONB,               -- {"01": 22.1, "02": 23.4, ...}
    avg_humidity_by_month JSONB            -- {"01": 45.0, "02": 48.0, ...}
);
```

---

## Section 17: Feed Storage & Quality Management

Feed quality degradation between the milling date and the point of consumption is a structurally unacknowledged problem in Kenyan broiler production. A study of local commercial feed samples in Kenya's Rift Valley found that 30–40% of feeds tested showed measurable mycotoxin contamination at levels capable of suppressing immune function and reducing weight gain by 5–15%.

### 17.1 Feed Storage Standards

| Parameter | Requirement | Consequence of Failure |
|---|---|---|
| **Maximum storage temperature** | < 25°C | Every 5°C rise above 25°C doubles the rate of fat oxidation (rancidity) and mycotoxin development |
| **Maximum relative humidity** | < 70% | Above 70% RH, grain moisture rises above 14%, triggering Aspergillus (aflatoxin) growth within 72 hours |
| **Maximum storage duration** | 6 weeks from milling date | Beyond 6 weeks: vitamin oxidation loss >20%, lysine degradation begins |
| **Light exposure** | Zero direct sunlight on bags | UV accelerates fat oxidation and vitamin A/D/E degradation |
| **Floor clearance** | Bags on pallets, minimum 15cm off floor | Prevents moisture wicking from concrete and rodent access |
| **Wall clearance** | Minimum 50cm gap between bags and wall | Enables air circulation and rodent monitoring |
| **Stack height** | Maximum 10 bags high | Prevents bag compression forcing oils to surface (promotes mold) |
| **FIFO discipline** | Oldest stock consumed first — mandatory | Mixed stock → oldest feed sits at back indefinitely |

### 17.2 Mycotoxin Risk Protocol

Mycotoxins (primarily Aflatoxin B1, Deoxynivalenol/DON, and Fumonisin) are invisible, odourless, heat-stable toxins produced by molds on maize and soybean — the primary ingredients in Kenyan commercial broiler feeds. They cannot be eliminated by heating or pelleting.

**Visual Red Flags (field assessment, no laboratory):**
- Clumped or caked feed in bags (moisture ingress)
- Feed smells musty, sour, or earthy (not the normal grain smell)
- Visible mold growth (green, black, or white patches) — this is extreme contamination
- Feed bags with holes (rodent contamination — rodents carry and spread mycotoxigenic molds)

**KukuFiti Mycotoxin Alert Triggers:**
If the system detects the following pattern over a 72-hour window: FCR rising >8% above target + feed intake declining >5% + no temperature anomaly → automatically flag "SUSPECTED MYCOTOXIN CONTAMINATION" and prompt manager to:
1. Log the current feed bag's batch/mill number
2. Quarantine remaining bags from that batch
3. Submit sample to Kenya Bureau of Standards (KEBS) or KARLO for aflatoxin testing (cost ~KES 2,500 per test)
4. Replace with feed from a different milling batch

```sql
CREATE TABLE feed_inventory (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id),
    phase VARCHAR(20) NOT NULL,             -- 'STARTER', 'GROWER', 'FINISHER_1', 'FINISHER_2'
    feed_brand VARCHAR(100) NOT NULL,       -- 'Unga Feeds', 'Pembe', 'Farmplus'
    mill_batch_number VARCHAR(100),
    milling_date DATE,
    delivery_date DATE NOT NULL,
    quantity_bags_received INT NOT NULL,
    weight_per_bag_kg NUMERIC(5,1) DEFAULT 50.0,
    cost_per_bag_kes NUMERIC(8,2) NOT NULL,
    storage_conditions_ok BOOLEAN DEFAULT TRUE,
    bags_remaining INT,
    quality_flag VARCHAR(20) DEFAULT 'NORMAL', -- 'NORMAL', 'SUSPECT', 'REJECTED', 'TESTED_OK'
    mycotoxin_test_result VARCHAR(100),
    notes TEXT
);
```

---

## Section 18: Harvest Optimization

The harvest decision is the highest-stakes single economic event in the broiler production cycle. Harvesting one week too early leaves significant live weight on the table. Harvesting one week too late, in a heat-stressed environment or falling market, can reverse an entire batch's profit.

### 18.1 Feed Withdrawal Protocol

Feed withdrawal before slaughter is legally required in Kenya under the Kenya Meat Commission standards, and biologically necessary to empty the digestive tract (preventing faecal contamination of carcasses during processing).

| Parameter | Standard | Notes |
|---|---|---|
| **Feed withdrawal duration** | 8–12 hours before slaughter | Do NOT exceed 12 hours — longer withdrawal causes birds to eat litter, increasing intestinal contents and contamination risk |
| **Water access** | Maintain water access until loading | Water prevents birds from eating litter during feed withdrawal |
| **Withdrawal timing** | Align feed removal with transport schedule | If slaughterhouse is 2 hours away, remove feed 9–10 hours before departure |
| **Documentation** | Log exact feed removal time in KukuFiti app | Required for food safety audit trail |

**The KukuFiti Harvest Timer** is a dedicated feature that, once triggered, displays a countdown to the loading window, sends alerts at T-12h (remove feed), T-2h (check birds for stress, prepare crates), and T-0h (begin catching).

### 18.2 Slaughter Weight Optimization Algorithm

The backend must run this optimization continuously from Day 28 onwards, querying current FCR trajectory, market price, and feed cost to determine the economically optimal harvest day:

```python
def calculate_optimal_harvest_day(
    current_fcr: float,
    daily_weight_gain_g: float,
    feed_cost_per_kg: float,
    market_price_kes_per_kg: float,
    current_day: int,
    current_live_weight_g: float,
    current_live_birds: int
) -> dict:
    """
    Marginal Return Analysis: harvest when the incremental revenue from
    one more day of growth is less than the incremental feed cost.
    
    Marginal revenue = daily_gain × market_price / 1000
    Marginal feed cost = daily_feed_g × feed_cost_per_kg / 1000
    Margin = marginal_revenue - marginal_feed_cost
    """
    results = {}
    for day in range(current_day, 43):
        projected_weight = current_live_weight_g + (daily_weight_gain_g * (day - current_day))
        revenue = (projected_weight / 1000) * market_price_kes_per_kg * current_live_birds
        
        # FCR deteriorates slightly with age (metabolic efficiency declining)
        age_fcr_penalty = (day - current_day) * 0.008
        feed_for_period = daily_weight_gain_g * (day - current_day) * (current_fcr + age_fcr_penalty)
        cost = (feed_for_period / 1000) * feed_cost_per_kg * current_live_birds
        
        results[day] = {
            "projected_weight_kg": round(projected_weight / 1000, 3),
            "projected_revenue_kes": round(revenue, 2),
            "additional_feed_cost_kes": round(cost, 2),
            "marginal_profit_kes": round(revenue - cost, 2)
        }
    
    optimal_day = max(results, key=lambda d: results[d]["marginal_profit_kes"])
    return {"optimal_harvest_day": optimal_day, "projections": results}
```

### 18.3 Carcass Yield Estimation

The relationship between live weight and dressed carcass weight determines the true value of the flock to a processing buyer.

| Metric | Formula | Standard Range |
|---|---|---|
| **Dressing percentage** | (Carcass weight / Live weight) × 100 | 72–76% for Cobb 500/Ross 308 |
| **Estimated carcass weight** | Live weight × 0.73 (conservative) | Higher FCR flock → lower dressing % |
| **Abdominal fat adjustment** | Increases with feed energy density and age | Day 42 birds average 1–2% higher fat content than Day 35 |

---

## Section 19: IoT Sensor Architecture

The KukuFiti system's intelligence engine is only as good as the quality and frequency of its sensor telemetry. This section defines the complete sensor network specification — sensor types, placement locations, sampling frequency, MQTT topic structure, and failover protocols.

### 19.1 Sensor Specifications

| Sensor Type | Parameter Measured | Model Recommendation | Accuracy | Placement | Count per House |
|---|---|---|---|---|---|
| **Temperature + Humidity** | Ambient temp (°C), RH (%) | DHT22 or SHT31 (higher accuracy) | ±0.5°C, ±2% RH | 4 corners + 1 centre, at bird level (0.5m AFF) | 5 |
| **Ammonia Gas** | NH3 concentration (ppm) | MQ-135 (field) or Membrapor NH3 (lab grade) | ±2 ppm | 2 per house, near litter in high-density zones | 2 |
| **CO2 Gas** | Carbon dioxide (ppm) | MH-Z19B NDIR sensor | ±50 ppm | 1 near fans, 1 at bird level | 2 |
| **Water Meter** | Flow rate (L/min), cumulative consumption | Pulse-output water meter (1L/pulse) | ±1% | Inline on main water supply line | 1 |
| **Load Cells** | Average live bird weight (g) | Platform scale with HX711 ADC | ±5g | 2 platforms per house, positioned near feeders | 2 |
| **Litter Moisture** | Litter moisture content (%) | Capacitive soil moisture sensor (adapted) | ±3% | 3 probes per house (near drinkers + centre) | 3 |
| **Light Sensor** | Lux level at bird level | BH1750 digital light sensor | ±3% | 1 per house, at bird level | 1 |
| **Fan Speed (RPM)** | Ventilation fan operational status | Hall-effect sensor on fan motor | On/Off + RPM | 1 per fan | Per-fan |

**Microcontroller:** ESP32 (dual-core, built-in WiFi and Bluetooth). One ESP32 node aggregates readings from all sensors in a zone (typically 2m² coverage) and publishes via WiFi to the MQTT broker.

### 19.2 MQTT Topic Structure

All sensor data is published to a hierarchical MQTT topic namespace. The KukuFiti FastAPI backend subscribes to all farm topics via an MQTT client (e.g., `aiomqtt` or `paho-mqtt`) running as an async background service.

```
kukufiti/
├── {farm_id}/
│   ├── {house_id}/
│   │   ├── sensors/
│   │   │   ├── temperature/{node_id}        → {"temp_c": 24.3, "rh_pct": 58.2, "timestamp": "2025-04-07T06:32:00Z"}
│   │   │   ├── gas/ammonia/{node_id}        → {"nh3_ppm": 12.4, "timestamp": "..."}
│   │   │   ├── gas/co2/{node_id}            → {"co2_ppm": 2840, "timestamp": "..."}
│   │   │   ├── water/flow/{node_id}         → {"flow_lpm": 4.2, "cumulative_l": 1240.5, "timestamp": "..."}
│   │   │   ├── weight/{platform_id}         → {"avg_weight_g": 1124.5, "sample_count": 47, "timestamp": "..."}
│   │   │   ├── litter/moisture/{probe_id}   → {"moisture_pct": 29.3, "timestamp": "..."}
│   │   │   └── light/{node_id}             → {"lux": 12.4, "timestamp": "..."}
│   │   ├── actuators/
│   │   │   ├── fans/{fan_id}               → {"state": "ON", "speed_pct": 75}
│   │   │   ├── brooders/{brooder_id}       → {"state": "ON", "output_pct": 60}
│   │   │   ├── lights/{zone_id}            → {"state": "ON", "dim_pct": 50}
│   │   │   └── foggers/{fogger_id}         → {"state": "OFF"}
│   │   └── alerts/
│   │       └── {alert_id}                  → {"severity": "CRITICAL", "rule": "HEAT_STRESS", "message": "..."}
│   └── farm/
│       └── status                          → {"active_batches": 2, "last_heartbeat": "..."}
```

### 19.3 Telemetry Ingestion & Moving Average Logic

The backend must compute 15-minute moving averages from individual 1-minute sensor readings before comparing against batch_targets thresholds. Raw 1-minute data is too noisy to drive actuations — a single anomalous reading should not trigger ventilation changes.

```python
# FastAPI background task: telemetry processing
async def process_telemetry_reading(farm_id: str, house_id: str, sensor_type: str, reading: dict):
    """
    1. Store raw reading in telemetry_raw table
    2. Compute 15-minute moving average
    3. Compare average to batch_target thresholds
    4. Trigger rule engine if threshold exceeded for 2+ consecutive averages (30 min sustained deviation)
    """
    await store_raw_reading(farm_id, house_id, sensor_type, reading)
    
    moving_avg = await compute_moving_average(farm_id, house_id, sensor_type, window_minutes=15)
    
    batch = await get_active_batch(farm_id, house_id)
    if batch:
        target = await get_batch_target(batch.id, batch.current_day)
        await evaluate_thresholds(batch, target, sensor_type, moving_avg)

```

```sql
CREATE TABLE telemetry_raw (
    id BIGSERIAL PRIMARY KEY,
    farm_id INT NOT NULL,
    house_id INT NOT NULL,
    batch_id INT REFERENCES batches(id),
    sensor_type VARCHAR(30) NOT NULL,
    node_id VARCHAR(50),
    reading_timestamp TIMESTAMPTZ NOT NULL,
    value_primary NUMERIC(10,4),            -- temp, NH3, CO2, flow, weight, moisture, lux
    value_secondary NUMERIC(10,4),          -- RH for temp/humidity sensors
    raw_payload JSONB                       -- Full MQTT payload for debugging
) PARTITION BY RANGE (reading_timestamp);  -- Time-based partitioning for performance

-- Create monthly partitions
CREATE TABLE telemetry_raw_2025_04 PARTITION OF telemetry_raw
    FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');
```

### 19.4 Sensor Failover Protocol

A sensor failing silently (returning no data) is more dangerous than a sensor reading incorrectly, because the backend may interpret silence as "no anomaly." The KukuFiti system must implement sensor health monitoring:

| Sensor State | Detection Method | System Response |
|---|---|---|
| **Healthy** | Reading received within last 5 minutes | No action |
| **Stale** | No reading for 5–15 minutes | ⚠️ WARN: "Sensor {node_id} data delayed. Check WiFi connectivity." |
| **Offline** | No reading for >15 minutes | 🚨 ALERT: "Sensor {node_id} OFFLINE. Manual monitoring required immediately." Last known reading displayed with age indicator. |
| **Out of Range** | Reading outside physically possible bounds (e.g., temp = -5°C or 80°C) | Flag as `SENSOR_FAULT`, exclude from moving average, alert for hardware inspection |

---

## Section 20: Emergency Protocols

Commercial poultry production faces categories of emergency that require pre-defined, automated responses. The KukuFiti system must maintain a library of emergency response protocols that are instantly surfaced through the application when critical conditions are detected.

### 20.1 Emergency Protocol Library

#### EP-001: Power Outage

The most catastrophic near-term emergency in Kenyan poultry production. KPLC (Kenya Power) outages lasting 4–6+ hours during Phase 3–4 can kill an entire flock through heat asphyxiation within 2–3 hours.

**Trigger:** Fan speed sensors report zero RPM while batch is active. OR IoT nodes go offline simultaneously (power outage signature).

**Automated Response Sequence:**
1. T+0: CRITICAL ALERT pushed to all registered farm contacts (owner, manager, vet)
2. T+0: App displays EP-001 checklist (pre-configured for this farm)
3. T+5 min: Manual confirmation prompt — "Is generator running? Y/N"
4. T+15 min (if no generator confirmation): Escalate alert to secondary contacts

**Pre-configured EP-001 Checklist:**
- [ ] Start backup generator immediately (location: [pre-configured field in farm profile])
- [ ] Open all curtain sidewalls manually to maximum if generator unavailable
- [ ] Move water containers into house to cool environment if birds showing heat stress
- [ ] Count and log birds found dead — document for insurance and post-event analysis
- [ ] Contact feed supplier / KPLC fault line
- [ ] Log power restoration time when grid returns

#### EP-002: Mass Mortality Event (>1% daily)

**Trigger:** `daily_logs.mortality_count / batches.initial_bird_count > 0.01` on any single day.

**Response:** Immediate biosecurity lockdown notification. Qualitative symptom collection form surfaced in app (bird posture, feces color, respiratory sounds). Backend cross-references Section 15 disease matrix and returns ranked differential diagnosis. Veterinary contact details displayed with one-tap call link.

#### EP-003: Market Price Collapse

**Trigger:** Farm manager manually inputs current market price, OR KukuFiti integrates with Kenya livestock price feed (AMIS or FAO GIEWS), and the entered price drops below the calculated break-even threshold for the current batch.

**Response:** Backend immediately runs the harvest optimization algorithm (Section 18.2) and presents three scenarios:
1. **Harvest now:** Current loss projection
2. **Extend by 7 days:** Projected outcome if prices recover (sensitivity range)
3. **Cold storage hedge:** If farm has or can access cold storage — cost vs. projected price recovery

#### EP-004: Feed Supply Disruption

**Trigger:** Feed inventory log shows fewer than 3 days' feed remaining for current flock size, AND no confirmed delivery scheduled.

**Response:** Alert with days-of-feed-remaining countdown. Supplier contact list displayed. Alternative local feed brand options (pre-populated from KukuFiti's localized database for Nakuru/Central Kenya region) displayed with last-known price and quality rating from inter-batch learning engine.

```sql
CREATE TABLE emergency_events (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id),
    event_timestamp TIMESTAMPTZ NOT NULL,
    protocol_code VARCHAR(20) NOT NULL,     -- 'EP_001', 'EP_002', 'EP_003', etc.
    trigger_source VARCHAR(50),             -- 'SENSOR_AUTO', 'MANUAL_REPORT'
    severity VARCHAR(20) NOT NULL,          -- 'WARNING', 'CRITICAL', 'CATASTROPHIC'
    duration_minutes INT,
    estimated_mortality_count INT,
    estimated_financial_loss_kes NUMERIC(12,2),
    resolution_actions TEXT,
    resolved_by VARCHAR(100),
    resolution_timestamp TIMESTAMPTZ,
    post_event_notes TEXT
);
```

---

## Section 21: Inter-Batch Machine Learning Engine

Every batch run by a KukuFiti farm generates a structured, timestamped dataset that is more valuable than the farm operator realizes. Over 5–10 batches, the system accumulates sufficient data to train lightweight predictive models that enable proactive, rather than reactive, farm management.

### 21.1 Feature Engineering (Input Variables)

The following features are extracted from completed batch records to train the inter-batch prediction models:

**Batch-Level Features:**
- Season (month of placement)
- Breed (Cobb 500 vs Ross 308)
- Initial bird count and stocking density (kg/m²)
- Chick supplier
- Starting uniformity CV (Day 7 weight sample)

**Environmental Features (averages by phase):**
- Mean ambient temperature per phase (actual vs. target deviation)
- Mean relative humidity per phase
- NH3 peak readings (ppm) per phase
- Total ventilation hours (≥50% fan capacity) per phase
- Number of days actual temp exceeded target by >2°C

**Nutritional Features:**
- Feed brand per phase
- Feed cost per kg by phase
- Average daily feed intake deviation from target (%)
- Water-to-feed ratio by week

**Health Features:**
- Vaccination completion (boolean per event)
- Coccidiosis treatment events count
- Disease treatment events count
- Water quality flags count

### 21.2 Prediction Targets

| Model | Target Variable | Business Value |
|---|---|---|
| **FCR Predictor** | Final cumulative FCR at harvest | Set procurement and pricing contracts more accurately |
| **Mortality Predictor** | Cumulative mortality % by Day 35 | Insurance, flock sizing, revenue projection |
| **Optimal Harvest Day** | Day that maximizes margin | Dynamic harvest scheduling |
| **Feed Brand Quality** | FCR contribution attributable to specific feed brand | Supplier scorecarding |
| **Disease Risk Classifier** | Probability of coccidiosis/NE outbreak by Day 21 | Pre-emptive coccidiostat dose adjustment |

### 21.3 Feed Brand Quality Scoring (Crowdsourced Regression)

This is the most commercially impactful feature of the inter-batch ML engine. Every batch where a specific feed brand is used and the final FCR is recorded creates one data point in a regression:

```
FCR_contribution_brand = actual_FCR - (baseline_FCR_for_conditions)

Where baseline_FCR accounts for: season, stocking density, mortality rate, and 
environmental management quality score — isolating the feed's independent effect.
```

After accumulating data across multiple farms (with user permission for anonymized sharing), the KukuFiti platform publishes a **Feed Brand Quality Index** — an empirical, market-specific ranking of every commercial feed brand available in Kenya, scored by actual biological outcomes rather than mill marketing claims.

```sql
CREATE TABLE batch_ml_features (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batches(id) UNIQUE,
    -- Batch metadata
    placement_month INT,
    breed VARCHAR(50),
    chick_supplier VARCHAR(100),
    initial_density_birds_m2 NUMERIC(5,2),
    -- Performance outcomes (populated at harvest)
    final_fcr NUMERIC(5,3),
    cumulative_mortality_pct NUMERIC(5,2),
    harvest_day INT,
    final_weight_g NUMERIC(7,2),
    net_profit_kes NUMERIC(12,2),
    -- Environmental quality scores (0-100, computed from daily logs)
    temp_management_score NUMERIC(5,2),
    humidity_management_score NUMERIC(5,2),
    ventilation_adequacy_score NUMERIC(5,2),
    -- Health events
    disease_events_count INT DEFAULT 0,
    antibiotic_treatment_days INT DEFAULT 0,
    coccidiosis_events_count INT DEFAULT 0,
    -- Feed data (denormalized from feed_inventory)
    starter_brand VARCHAR(100),
    grower_brand VARCHAR(100),
    finisher_brand VARCHAR(100),
    blended_feed_cost_per_kg NUMERIC(8,2),
    -- Computed at batch close
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Feed brand performance view (requires 5+ batches per brand for statistical validity)
CREATE MATERIALIZED VIEW feed_brand_performance AS
SELECT 
    starter_brand AS brand,
    'STARTER' AS phase,
    COUNT(*) AS batch_count,
    AVG(final_fcr) AS avg_fcr,
    STDDEV(final_fcr) AS fcr_stddev,
    AVG(net_profit_kes) AS avg_profit_kes,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY final_fcr) AS median_fcr
FROM batch_ml_features
WHERE starter_brand IS NOT NULL
GROUP BY starter_brand
UNION ALL
SELECT grower_brand, 'GROWER', COUNT(*), AVG(final_fcr), STDDEV(final_fcr), 
       AVG(net_profit_kes), PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY final_fcr)
FROM batch_ml_features
WHERE grower_brand IS NOT NULL
GROUP BY grower_brand
UNION ALL
SELECT finisher_brand, 'FINISHER', COUNT(*), AVG(final_fcr), STDDEV(final_fcr),
       AVG(net_profit_kes), PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY final_fcr)
FROM batch_ml_features
WHERE finisher_brand IS NOT NULL
GROUP BY finisher_brand;
```

---

## Section 22: Expanded FastAPI Endpoint Specification

This section extends the API architecture from Section 7 with the complete endpoint map covering all modules introduced in Sections 8–21.

### 22.1 Complete Endpoint Map

```
/api/v1/
├── auth/
│   ├── POST   /register                           → Farm owner registration
│   ├── POST   /login                              → JWT token issuance
│   └── POST   /refresh                            → Token refresh
│
├── farms/
│   ├── POST   /                                   → Create farm profile + GPS location
│   ├── GET    /{farm_id}                          → Farm dashboard summary
│   └── PATCH  /{farm_id}/location                 → Update GPS, altitude, climate zone
│
├── batches/
│   ├── POST   /                                   → Create new batch (requires HOUSE_READY checklist)
│   ├── GET    /{batch_id}                         → Full batch status + KPI dashboard
│   ├── GET    /{batch_id}/readiness               → Pre-placement checklist completion
│   ├── POST   /{batch_id}/activate                → Activate batch after checklist complete
│   └── POST   /{batch_id}/close                   → Close batch at harvest
│
├── checklist/
│   ├── GET    /{batch_id}/pre-placement           → Full pre-placement checklist
│   └── PATCH  /{batch_id}/pre-placement/{task_id} → Mark task complete (+ photo upload)
│
├── telemetry/
│   ├── POST   /environment                        → MQTT ingestion: temp + humidity
│   ├── POST   /gas                                → MQTT ingestion: NH3 + CO2
│   ├── POST   /water-flow                         → MQTT ingestion: water meter pulse
│   ├── POST   /weight                             → MQTT ingestion: load cell average
│   ├── GET    /{batch_id}/current                 → Latest 15-min averages for all sensors
│   ├── GET    /{batch_id}/history                 → Time-series data (with date range filter)
│   └── GET    /{batch_id}/sensor-health           → Sensor online/offline/fault status
│
├── logs/
│   ├── POST   /daily                              → Daily manual log (mortality, feed, water, samples)
│   ├── GET    /{batch_id}/daily                   → All daily logs for batch
│   ├── POST   /litter                             → Litter assessment log
│   ├── POST   /water-quality                      → Water quality test results
│   └── POST   /biosecurity                        → Visitor/vehicle biosecurity log
│
├── weights/
│   ├── POST   /{batch_id}/sample                  → Manual weight sample entry (N birds)
│   └── GET    /{batch_id}/uniformity              → CV, grade, trend chart data
│
├── vaccinations/
│   ├── GET    /{batch_id}/schedule                → Full vaccination schedule with countdown
│   └── POST   /{batch_id}/record                  → Log completed vaccination event
│
├── feed/
│   ├── POST   /{batch_id}/inventory               → Log feed delivery (brand, batch, cost, qty)
│   ├── GET    /{batch_id}/inventory               → Current feed stock by phase
│   ├── GET    /brands/performance                 → Feed brand quality index (all farms)
│   └── POST   /{batch_id}/withdrawal/start        → Trigger harvest feed withdrawal timer
│
├── thinning/
│   ├── POST   /{batch_id}/event                   → Log partial harvest / thinning event
│   └── GET    /{batch_id}/density                 → Current density calculation + thinning recommendation
│
├── analytics/
│   ├── GET    /{batch_id}/deviations              → All active threshold breaches with severity
│   ├── GET    /{batch_id}/fcr                     → Real-time FCR + projected final FCR
│   ├── GET    /{batch_id}/mortality-trend         → Mortality decay curve vs. actual
│   ├── GET    /{batch_id}/ammonia-risk            → Computed ammonia risk score from litter + temp
│   └── GET    /{batch_id}/optimal-harvest         → Marginal return harvest day calculator
│
├── financial/
│   ├── GET    /{batch_id}/projection              → P&L projection at current FCR trajectory
│   ├── GET    /{batch_id}/break-even              → Break-even market price per kg
│   ├── POST   /{batch_id}/price-scenario          → Run sensitivity scenario with new price input
│   └── GET    /{batch_id}/thinning-revenue        → Cumulative revenue from partial harvests
│
├── planning/
│   ├── GET    /batch-start-calendar               → Optimal start date recommendations by season
│   └── GET    /batch-capacity/{farm_id}           → Max birds per house based on m², breed, season
│
├── emergencies/
│   ├── POST   /{batch_id}/declare                 → Manually declare emergency event
│   ├── GET    /{batch_id}/protocols               → Available emergency protocol library
│   └── PATCH  /{batch_id}/emergencies/{event_id} → Update resolution status
│
└── ml/
    ├── GET    /{batch_id}/risk-scores             → Disease + mortality risk prediction scores
    ├── GET    /feed-brand-index                   → Crowdsourced feed brand performance table
    └── GET    /{farm_id}/batch-comparison         → Compare all closed batches (trends, FCR, profit)
```

### 22.2 Pydantic Schema Additions

```python
from pydantic import BaseModel, validator, Field
from datetime import date, datetime
from typing import Optional, Literal
from decimal import Decimal

class DailyLogCreate(BaseModel):
    batch_id: int
    log_date: date
    actual_temp_avg: Optional[Decimal] = Field(None, ge=-5, le=45, description="°C")
    actual_rh_avg: Optional[Decimal] = Field(None, ge=0, le=100, description="%")
    feed_consumed_kg: Optional[Decimal] = Field(None, ge=0)
    water_consumed_l: Optional[Decimal] = Field(None, ge=0)
    mortality_count: int = Field(0, ge=0)
    cull_count: int = Field(0, ge=0)
    sample_weight_avg_g: Optional[Decimal] = Field(None, ge=0)
    qualitative_notes: Optional[str] = None
    
    @validator('mortality_count')
    def mortality_must_be_reasonable(cls, v, values):
        return v  # Backend cross-checks against flock size

class WeightSampleCreate(BaseModel):
    batch_id: int
    sample_date: date
    birds_sampled: int = Field(..., ge=10, description="Minimum 10 birds for statistical validity")
    individual_weights_g: list[float] = Field(..., description="Array of individual bird weights")
    
    @validator('individual_weights_g')
    def compute_statistics(cls, v, values):
        if len(v) != values.get('birds_sampled', 0):
            raise ValueError("Weight array length must match birds_sampled")
        return v  # Backend computes mean, std_dev, CV

class HarvestOptimizationRequest(BaseModel):
    batch_id: int
    current_market_price_kes_per_kg: Decimal = Field(..., ge=100, le=500)
    price_scenario_min: Optional[Decimal] = None  # For sensitivity range
    price_scenario_max: Optional[Decimal] = None

class EmergencyDeclare(BaseModel):
    batch_id: int
    protocol_code: Literal['EP_001', 'EP_002', 'EP_003', 'EP_004', 'EP_005']
    trigger_source: Literal['SENSOR_AUTO', 'MANUAL_REPORT']
    severity: Literal['WARNING', 'CRITICAL', 'CATASTROPHIC']
    initial_description: str
```

---

# APPENDICES

## Appendix A: Complete Enhanced Database Schema Summary

All tables introduced across all sections, consolidated for implementation reference:

| Table | Section | Purpose |
|---|---|---|
| `breeds` | 7 | Breed definitions with genetic FCR targets |
| `batches` | 7 | Batch lifecycle with farm, breed, and status |
| `batch_targets` | 7 | 42-day biological target matrix — immutable ground truth |
| `daily_logs` | 7 | Time-series repository for manual + aggregated sensor data |
| `batch_performance_kpis` (MAT. VIEW) | 7 | Real-time FCR, mortality, and live bird calculations |
| `pre_placement_checklist` | 8 | 14-day house preparation task tracker |
| `batch_readiness` (VIEW) | 8 | Batch activation gate — all tasks must be complete |
| `water_quality_logs` | 9 | Weekly water parameter test results |
| `litter_assessments` | 10 | Litter moisture, caking, and treatment records |
| `lighting_programs` | 11 | Per-day lighting schedule (hours, lux) |
| `lighting_actuations` | 11 | IoT relay log for light control events |
| `weight_samples` | 12 | Weight sample records with CV and uniformity grade |
| `thinning_events` | 13 | Partial harvest records with revenue and density |
| `biosecurity_log` | 14 | Visitor, vehicle, and zone access log |
| `vaccination_events` | 15 | Scheduled and completed vaccination records |
| `farm_location` | 16 | GPS, altitude, climate zone, seasonal temperature/humidity profile |
| `feed_inventory` | 17 | Feed delivery, stock, quality flag, mycotoxin records |
| `emergency_events` | 20 | Emergency incident log with resolution and financial impact |
| `batch_ml_features` | 21 | Feature-engineered batch outcomes for ML model training |
| `feed_brand_performance` (MAT. VIEW) | 21 | Crowdsourced feed brand FCR quality index |
| `telemetry_raw` (PARTITIONED) | 19 | High-volume time-series sensor telemetry |

---

## Appendix B: Production Deployment Checklist (Railway)

For the KukuFiti backend deployed to Railway, the following environment variables and services must be configured:

```env
# Core Application
DATABASE_URL=postgresql://...
SECRET_KEY=<256-bit random string>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# MQTT Broker (for IoT sensor integration)
MQTT_BROKER_HOST=<broker.hivemq.com or self-hosted>
MQTT_BROKER_PORT=8883
MQTT_USERNAME=<farm_mqtt_user>
MQTT_PASSWORD=<mqtt_password>
MQTT_TLS_ENABLED=true

# Background Tasks
CELERY_BROKER_URL=redis://...
TELEMETRY_PROCESSING_INTERVAL_SECONDS=60
ALERT_EVALUATION_INTERVAL_SECONDS=300

# Notifications
AFRICASTALKING_API_KEY=<key>          # SMS alerts for Kenya
AFRICASTALKING_USERNAME=<username>
FCM_SERVER_KEY=<key>                  # Push notifications to Flutter app

# File Storage (for pre-placement photos)
CLOUDINARY_CLOUD_NAME=<name>
CLOUDINARY_API_KEY=<key>
CLOUDINARY_API_SECRET=<secret>

# Seasonal Data
FARM_GPS_LAT=-0.303099               # Default: Nakuru
FARM_GPS_LNG=36.080026
FARM_ALTITUDE_M=1850
```

---

## Document Metadata

| Field | Value |
|---|---|
| **Document Title** | KukuFiti Framework — Godmode Enhancement: Complete Operational Intelligence Supplement |
| **Base Document** | Architectural and Agronomic Blueprint for Real-Time Broiler Production Intelligence |
| **Version** | 2.0 (Consolidated) |
| **Sections** | 1–22 + Appendices A–B |
| **Target Stack** | FastAPI + PostgreSQL (Railway Deployment) |
| **Target Market** | Kenya / East Africa Commercial Broiler Production |
| **Primary Breeds** | Cobb 500, Ross 308 |
| **Altitude Profile** | Nakuru, Kenya — 1,850m ASL |
| **Currency Reference** | Kenyan Shilling (KES), 2025/2026 Market Horizon |

---

*End of Consolidated KukuFiti Framework Document*
