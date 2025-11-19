# Aixavier Edge Analytics – US Multi-Vertical Business Model

*(Use-Case–First, Hardware-Agnostic, Wedge-Vertical Strategy)*

## 0. Executive Summary

1. **What we are** – A **use-case–driven, hardware-agnostic edge video analytics platform** that runs on multiple edge compute backends (NVIDIA GPUs, x86/NVRs, industrial PCs, and, where possible, smart cameras / ARM SoCs) and turns CCTV streams into **real-time safety, security, and operations signals**.

2. **Core IP & moat** – A **cross-vertical pattern catalog** (restricted zones, person-down, crowding, aggression, PPE, equipment misuse, smoke/fire), plus **rules/templates, KPIs, and deployment playbooks** and orchestration tooling. The value is in **patterns + rules + playbooks + deployment**, not in any particular hardware box.

3. **Where we start (wedges)** – Focused for the first 2–3 years on:

   * **Transit & Mobility** (on-vehicle and station safety/ops), and
   * **Warehousing & Logistics** (DC/3PL/e-commerce safety & throughput),
     with **Retail, Smart City, and Industrial/Critical Infrastructure** as medium-term expansion.

4. **Hardware strategy** – Architecture is **multi-backend by design**, rolled out in phases:

   * **Phase 0:** NVIDIA + common x86 edge devices (current implementation focus).
   * **Phase 1:** x86 / NVR / industrial PCs as a lightweight service.
   * **Phase 2:** selective **camera OEM / ARM SoC** integrations for smart cameras.

5. **Market** – We model a US **analytics node TAM ≈ 100–190k nodes** (midpoint ~150k). At an assumed **$3,000/node/year**, this corresponds to **~$300–570M ARR**, midpoint **≈$450M ARR**, for the **edge-side safety & operations analytics** slice of the US video analytics market.

6. **SAM (5–7 years)** – Focused on our wedges plus a small number of lighthouse deployments:

   * **~25–30k nodes**, i.e. **~$75–90M ARR** at **$3k/node/year**.

7. **5-year US scenarios (SOM)**
   At $3,000/node/year, US-only:

   * **Scenario 1 – Conservative (low case):**
     Y5 **10–12k nodes** ⇒ **$30–36M ARR** (~30–50% SAM).
   * **Scenario 2 – Base (mid case):**
     Y5 **15–18k nodes** ⇒ **$45–54M ARR** (~50–65% SAM).
   * **Scenario 3 – Aggressive (high case):**
     Y5 **25–30k nodes** ⇒ **$75–90M ARR**, approaching full SAM.

8. **Economics** – We model **$3,000/node/year** realised ARR and target **75–80% gross margins** at scale, with heavy compute at the **edge** and the **cloud** used for control-plane, logging, and fleet management.

9. **GTM** – **Wedge-driven**: high-impact pilots in transit and warehousing, packaged into **vertical playbooks**, then scaled via **system integrators and OEMs** as the “safety/ops intelligence layer” on top of existing camera+VMS stacks.

10. **Why now** – Rising **incident and liability costs**, growing **regulatory and stakeholder pressure**, **edge compute + models** now strong enough for multi-stream analytics, and increasing discomfort with **shipping raw video to the cloud**.

> **Naming note:** *“Aixavier” is a working internal codename inherited from an earlier Jetson-focused implementation. The eventual commercial brand will **not** be tied to any specific hardware vendor.*

---

## 1. Positioning & Scope (Use-Case–First, Wedge Verticals)

### 1.1 What Aixavier Is

**Aixavier Edge Analytics** is a **use-case–driven edge video analytics platform** that runs on multiple edge compute backends and turns raw CCTV streams into **actionable safety, security, and operations signals**.

**Core IP =**

* A **catalog of domain-specific use cases** grouped into **generic detection patterns** (Section 2).
* A **rules and policy engine** (zones, thresholds, schedules, workflows).
* **Orchestration & deployment tooling**:

  * Model pipelines and configs per site/vertical.
  * Fleet-wide rollout, monitoring, and over-the-air updates.
* **Integrations**:

  * Existing cameras.
  * Existing **VMS/NVR** stacks.
  * Incident, ticketing, and safety systems.

**What we are not:**

* Not a “Jetson box company” or tied to a single hardware SKU.
* Hardware (edge box, NVR, smart camera) is **replaceable plumbing**; our IP sits **above** it.

### 1.2 Wedge Verticals (First 2–3 Years)

We intentionally begin with **two wedge verticals** where:

* Safety & operations pain is visible and costly.
* Camera density is high.
* Edge constraints (bandwidth, privacy, latency) are real.

**Transit / Mobility (Wedge #1)**

* On-vehicle: railcars, buses, shuttles, people-movers.
* Fixed nodes: stations, depots, yards, terminals, park-and-rides.
* Patterns: crowding, trespass, aggression/assault, slip/fall, unsafe boarding/alighting, suspicious/unattended objects.

**Warehousing & Logistics (Wedge #2)**

* Distribution centres, 3PLs, e-commerce hubs, big-box DC networks.
* Patterns: forklift/people conflict, PPE compliance, restricted zones, dock congestion, yard intrusion, unsafe material handling.

These wedges give us:

* **Strong ROI narratives** (injury reduction, claim reduction, throughput gains).
* Sites that can justify **incremental analytics spend** per camera/node.
* Clear opportunities for **repeatable playbooks**.

### 1.3 Medium-Term Expansion Verticals

These are **explicitly medium-term**, not day-one priorities:

* **Retail & Consumer Venues** – large-format stores, malls, stadiums, arenas, casinos.
* **Smart Cities & Public Safety** – intersections, public spaces, transit hubs.
* **Critical Infrastructure & Industrial** – utilities, refineries, ports, airports’ airside, large manufacturing plants, data centres.

Strategy:

* 1–3 **lighthouse customers per vertical** to validate patterns and build reference stories.
* **Scale only after** wedge vertical playbooks and unit economics are proven.

### 1.4 Hardware Strategy – Phased, Multi-Backend

The architecture is **multi-backend by design**. Implementation rollout:

* **Phase 0 (current)** – NVIDIA-based edge devices & common x86 appliances

  * Most mature stack (CUDA, TensorRT, ONNX, Docker).
  * Current model pipelines and deployment tooling are furthest along here.

* **Phase 1** – x86 / NVR / industrial PCs

  * Ship a **lightweight edge runtime service** on standard NVRs and industrial PCs (CPU-only or CPU+GPU).
  * Leverages hardware already deployed in many DCs and transit control rooms.

* **Phase 2** – Selected camera OEMs / ARM SoCs / smart cameras

  * Integrations via camera SDKs or ONVIF extensions.
  * Host **lightweight models or metadata-emitting agents** on smart cameras.
  * Selective: only high-volume OEMs / platforms to keep focus.

**Key message:** current implementation is furthest along on **Phase 0**, but the **software architecture, APIs, and deployment model are explicitly multi-backend** and built to span all three phases.

---

## 2. Use-Case Catalog as Generic Patterns & Playbook Moat

We start from an initial set of **22 rail-flavoured use cases** and generalise them into **8 canonical detection patterns** that apply across verticals.

### 2.1 The 8 Canonical Patterns (with examples)

1. **Restricted-Zone Intrusion**

   * Person or object enters a pre-defined no-go zone.
   * **Transit example:** passenger steps off platform edge into track area; unauthorized person in tunnel.
   * **Warehouse example:** worker walks into forklift-only aisle or behind a reversing truck.

2. **Unattended / Suspicious Object**

   * Object left unattended beyond a time threshold in a sensitive context.
   * **Transit:** suitcase left on platform staircase or near ticket gates.
   * **Warehouse:** pallet or box left blocking emergency exit or fire door.

3. **Person-Down / Fall / Collapse**

   * Human appears to fall or lies motionless in concerning posture.
   * **Transit:** passenger collapses in railcar; person lying on platform.
   * **Warehouse:** worker falls off loading dock; person down in aisle.

4. **Crowding / Over-Capacity / Queues**

   * Density passes a threshold or queues exceed length/time thresholds.
   * **Transit:** platform over-crowding at peak; blocked entrances; dwell-time overruns due to slow boarding.
   * **Retail/logistics:** long checkout queues; congested dock area or staging lanes.

5. **Aggression / Violence / Fighting**

   * Rapid or repeated aggressive movements suggestive of fighting or assault.
   * **Transit:** altercation in subway car; passenger assault at station entrance.
   * **Stadium/warehouse:** fight in concourse; physical altercation in warehouse break area.

6. **Staff Compliance & Presence**

   * Expected staff position, attire, or behaviour vs defined rule.
   * **Transit:** no staff present at required door during boarding; platform unattended during dwell.
   * **Warehouse:** workers in high-risk zone without hi-vis/PPE; missing spotter near reversing truck.

7. **Equipment Misuse & Unsafe Operation**

   * Machine or vehicle used outside safe envelope.
   * **Transit:** train doors held open; door forced while moving; person riding outside safe area.
   * **Warehouse:** forklift speeding; carrying passengers; elevated load near pedestrians; machine operated with guard removed.

8. **Environmental & Smoke/Fire Anomalies**

   * Visible smoke, haze, flame, or unusual environmental patterns.
   * **Transit:** smoke in railcar; small fire in platform trash bin.
   * **Industrial/warehouse:** smoke near battery racks; haze in hazardous storage area.

### 2.2 Mapping the Original 22 Use Cases

The original **22 rail-centric use cases** map directly into these patterns, for example:

* “Person on tracks” → **Restricted-zone intrusion**.
* “Passenger collapse on platform” → **Person-down**.
* “Door obstruction / door held” → **Equipment misuse & unsafe operation**.
* “Unattended luggage” → **Unattended / suspicious object**.
* “Platform overcrowding” → **Crowding / queues**.

This mapping shows we’re not tied to **rail semantics**; we’re encoding **underlying safety/ops patterns**.

### 2.3 Why This Is More Than a List of Use Cases

The pattern catalog is **not just a list of names**. The moat is in the **operationalisation**:

For each pattern, we maintain:

* **Rules & templates per vertical**

  * Zone definitions (e.g., “red zone” near platform vs around conveyors).
  * Time thresholds, sensitivity levels, schedule templates (e.g., peak vs off-peak).
  * Combinational logic (e.g., person + elevated forklift load in the same region).

* **KPI definitions & analytics**

  * Incident rate per **10k operating hours**.
  * **Mean time to detect** (MTTD) and **mean time to respond** (MTTR).
  * False alarm rates per site per day.
  * Pre/post comparisons for deployments (e.g., reduction in undetected person-down events or investigation time).

* **Deployment templates**

  * Recommended camera placements by vertical.
  * Example **node sizing** (how many streams per node).
  * Integration best practices with existing VMS/NVR per pattern.

* **Continuous improvement loop**

  * Feedback from real incidents (true positives, false positives/negatives, near-misses).
  * Roll these into:

    * Model re-tuning or re-selection.
    * Rule and threshold adjustments.
    * Updated deployment playbooks.

> **Net effect:** The combination of **pattern catalog + rules/templates + KPIs + deployment recipes + feedback loop** becomes a **playbook IP** layer that is hard to copy by simply “adding more detectors.”

---

## 3. US Market Landscape & Node TAM

### 3.1 Macro Context – Video Surveillance & Analytics

* The **US video surveillance market** is projected to reach **≈$37B by 2030**, with an ~**11–12% CAGR**. *(Grand View Research)*
* The **global video analytics market** is estimated at **≈$10.25B in 2024**, projected to grow to **≈$49B by 2032**, with **North America ~33%** of the market. *(Fortune Business Insights)*
* Another estimate puts **North American video analytics** at **≈$4.9B in 2024**. *(Precedence Research)*

We focus on the **subset** of that market that:

* Runs **in or very close to the edge** (vehicle/station/DC/plant).
* Delivers **safety and operations** value (not just generic security or marketing analytics).

We define an **analytics node** as:

* A logical edge runtime instance handling roughly **4–16 camera streams**, depending on:

  * Resolution and frame rate.
  * Model complexity and number of patterns enabled.
  * Hardware configuration.

### 3.2 TAM by Vertical (Node Ranges & Assumptions)

#### 3.2.1 Transit / Mobility (Wedge Vertical #1)

**Facts (directional):**

* Amtrak operates **2,142 railcars and 425 locomotives**. *(Wikipedia)*
* US freight railroads invest **>$23B/year** in infrastructure and equipment. *(Association of American Railroads)*
* US transit agencies operate dozens of **metro, light rail, commuter rail, BRT, and large bus fleets**, plus **thousands of stations and depots**. *(APTA and related sources)*

**Working assumptions:**

* Only a **subset of vehicles** will be equipped with on-board analytics within our horizon.
* Not every small stop/station warrants a full node; major stations and depots do.

**Node TAM estimate:**

* **On-vehicle nodes**:

  * Targeted railcars, locomotives, large buses, and airport people-movers.
  * Many vehicles share one analytics node (per consist/fleet segment).
  * We model **~15–25k nodes** across US transit, intercity passenger rail, airport shuttles, and key bus fleets.

* **Fixed-site nodes**:

  * Major stations, depots, yards, park-and-rides, terminals.
  * Larger sites need **1–3 nodes** depending on layout and camera count.
  * We model **~5–10k nodes**.

> **Transit / Mobility node TAM:** **≈20–35k nodes**.
> **Assumptions:** partial vehicle coverage, major sites only, 1–3 nodes per significant station/yard.

#### 3.2.2 Warehousing & Logistics (Wedge Vertical #2)

**Facts (directional):**

* Some sources estimate **≈22k warehouses** in the US; broader definitions (including smaller e-commerce facilities) push this much higher, up toward **~100–150k** depending on thresholds for size and use.
* Warehouse sizes, complexity, and tech maturity vary widely.

To avoid false precision:

* We treat US warehouses/DCs as **≈40–60k sites** of varying size and tech maturity.

**Working assumptions:**

* Only **20–30%** of sites are **large and mature enough** to adopt advanced edge analytics within our 5–7 year horizon.

  * That yields **~8–18k candidate warehouses**.
* Each candidate site uses **2–4 analytics nodes**:

  * One for dock/yard, one for aisles/conveyors, possibly others for mezzanines or high-value areas.

**Node TAM estimate:**

> **Warehousing & Logistics node TAM:** **≈20–40k nodes**.
> **Assumptions:** 20–30% of all warehouses are viable; 2–4 nodes per viable site.

#### 3.2.3 Retail & Consumer Venues (Expansion, Upside)

**Facts (directional):**

* Including non-store retailers and sole proprietors, there are **≈2.8M retailers** in the US. *(Capital One Shopping)*
* In-store sales still account for **≈81.6% of US retail revenue** in 2024 (~$7.27T). *(Capital One Shopping)*

We are **not** targeting every store; only **large, complex, high-traffic** venues:

* Big-box stores.
* Malls and shopping centres.
* Stadiums, arenas, large casinos.

**Working assumptions (illustrative; not driving SAM):**

* Treat **2–3%** of retailers as “analytics-rich, large venues” ⇒ **~50–80k sites**.
* Each site uses **1–3 nodes** for entrances, concourses, high-loss zones.

> **Retail & Consumer Venues node TAM:** **≈50–80k nodes (illustrative)**.
> This is **future upside**, **not** core to the 5–7 year SAM/SOM; used as an order-of-magnitude sense-check.

#### 3.2.4 Smart Cities & Public Safety (Expansion)

Target: US cities and metros with **CCTV-rich public safety programs**.

**Working assumptions:**

* **10–20 major metros** and regional hubs are realistic candidates.
* Each may ultimately deploy **50–300 nodes**:

  * Intersections, public squares, transit hubs, tourist districts, etc.

> **Smart City node TAM:** **≈1–5k nodes**.

#### 3.2.5 Critical Infrastructure & Industrial (Expansion)

Includes:

* Utilities, refineries, power plants.
* Ports, airports’ airside, large logistics hubs.
* Large manufacturing plants and data centres.

**Working assumptions:**

* **~3–5k sites** are high-value enough to justify advanced analytics within our horizon.
* Each uses **2–6 nodes**.

> **Industrial & Critical Infrastructure node TAM:** **≈10–30k nodes**.

### 3.3 Aggregate US Node TAM

Summing the ranges:

* Transit / Mobility: **20–35k**
* Warehousing & Logistics: **20–40k**
* Retail & Consumer Venues: **50–80k** (future upside)
* Smart Cities: **1–5k**
* Industrial / Critical Infrastructure: **10–30k**

> **Total US analytics node TAM:** **≈100–190k nodes**.
> For modelling we use a midpoint of **~150k nodes**.

### 3.4 $-TAM and Sanity Check vs Existing Players

Using **$3,000/node/year** as our working pricing assumption:

> **US ARR TAM:** **≈$300–570M/year**, with a working midpoint of **≈$450M/year** for the **edge-side safety & ops analytics** segment.

**Sanity check vs existing players:**

* Cloud camera platforms (e.g. Verkada/Meraki-class vendors) and **vertical safety-AI startups** in PPE/forklift/zone safety already reach **meaningful tens to hundreds of millions** in ARR across adjacent segments.
* We use their scale as an **order-of-magnitude benchmark**, not a precise target:

  * We are focused on **edge-centric**, **multi-vertical patterns** and **integration with existing VMS/NVR stacks** rather than replacing them.

---

## 4. TAM → SAM → SOM (Wedge-Focused Logic)

### 4.1 TAM – Theoretical Ceiling

* **TAM (nodes):** all theoretically reachable nodes across our identified verticals, **≈100–190k**, midpoint **~150k**.
* **TAM (ARR):** at $3k/node/year, **≈$300–570M**, midpoint **~$450M**.

### 4.2 SAM – Serviceable Available Market (5–7 Year Horizon)

We define **SAM** as:

* What we can **reasonably** address in the US in **5–7 years**,
* Given our wedge focus, product roadmap, and channel strategy.

**SAM focus:**

* **Primary wedges:** Transit / Mobility and Warehousing & Logistics.
* **Plus:** limited lighthouse projects in Retail, Smart City, Industrial.

**Node SAM:**

* Transit / Mobility: **~10–15k nodes** (highest-value lines, depots, yards, key fleets).
* Warehousing & Logistics: **~10–15k nodes** (large DCs, e-commerce hubs, 3PL hubs, big-box DC networks).
* Lighthouse: **~1–3k nodes** across Retail, Smart City, Industrial.

> **US SAM (nodes, 5–7 yrs):** **≈25–30k nodes**.
> At **$3k/node/year**, **SAM ARR ≈ $75–90M/year**.

### 4.3 SOM – 5-Year Adoption Path (Three Scenarios)

SOM is our **actual modeled adoption** in 5 years, always ≤ SAM.

#### Scenario 1 – Conservative (Low Case)

* **Node adoption (EOY, US):**
  Y1: **500**
  Y2: **2,000**
  Y3: **6,000**
  Y4: **9,000**
  Y5: **10–12k** nodes

* **ARR at $3k/node/year:**
  Y1: **$1.5M**
  Y2: **$6.0M**
  Y3: **$18.0M**
  Y4: **$27.0M**
  Y5: **$30–36M**

* **SAM penetration (nodes):** ~30–50% by Year 5.

**Assumption sketch (Conservative):**

* Sales cycles: **18–24 months** for large agencies and national DC networks.
* **3–5 substantial pilots/year**, some constrained by budget cycles.
* Pilot → rollout conversion: **~30–40%**, with rollouts often partial estates.

#### Scenario 2 – Base (Mid Case)

* **Node adoption (EOY, US):**
  Y1: **1,200**
  Y2: **4,000**
  Y3: **9,000**
  Y4: **13,000**
  Y5: **15–18k** nodes

* **ARR at $3k/node/year:**
  Y1: **$3.6M**
  Y2: **$12.0M**
  Y3: **$27.0M**
  Y4: **$39.0M**
  Y5: **$45–54M**

* **SAM penetration (nodes):** ~50–65% by Year 5.

**Assumption sketch (Base):**

* Sales cycles: **12–18 months** for big transit deployments; shorter for private DC networks.
* Pilots: **5–10 meaningful pilots/year**, split between transit and logistics.
* Pilot → rollout conversion: **~50–60%**, where “rollout” = at least one significant corridor/fleet segment or region of DCs.

#### Scenario 3 – Aggressive (High Case)

* **Node adoption (EOY, US):**
  Y1: **2,500**
  Y2: **8,000**
  Y3: **16,000**
  Y4: **24,000**
  Y5: **25–30k** nodes

* **ARR at $3k/node/year:**
  Y1: **$7.5M**
  Y2: **$24.0M**
  Y3: **$48.0M**
  Y4: **$72.0M**
  Y5: **$75–90M**

* **SAM penetration (nodes):** approaches full SAM by Year 5.

**Assumption sketch (Aggressive):**

* Sales cycles compress to **9–15 months** due to strong references, standardised offerings, and channel leverage.
* Pilots: **10–15 pilots/year** run in parallel, in partnership with major SIs and OEMs.
* Pilot → rollout conversion: **~60–70%**, with more **multi-site / multi-corridor** rollouts per win.

---

## 5. Pricing & Unit Economics

### 5.1 Licensing Model – Node-Based, Customer-Friendly

We **model** revenue as:

> **$3,000 per node per year (ARR)**

…which corresponds to:

* Core platform.
* One vertical pattern pack.
* Some portion of premium features.
* Net of typical discounts.

**Market reality:**

* Today, analytics and cloud camera platforms are typically priced:

  * **Per camera** (e.g. $X/camera/month).
  * **Per site** (flat price per store, warehouse, station).
  * **Per device** (per NVR or edge box).

Many mature offerings land in the **hundreds of dollars per camera per year** in effective price when you unpack their SKU structure. For **4–16 cameras per node**, our **$3k/node** assumption sits in a **similar effective band**, depending on stream density and feature mix.

**Commercial packaging:**

* Internally, we track revenue **per node** for modeling, ops, and channel planning.
* Customer-facing, we expect to offer:

  * **Per-site** pricing (e.g. per warehouse, per station).
  * **Per-camera bundles** for some segments.
  * Or **hybrid** models (site minimum + camera add-ons).

Early pilots will be used to:

* Test willingness-to-pay.
* Determine which packaging feels **natural** to buyers and integrators.
* Align with existing budget categories.

### 5.2 COGS & Gross Margin

We aim for **infrastructure-style gross margins** once the platform is mature.

**Target GM:** **~75–80%**

**Working COGS per node-year:**

* **Cloud infrastructure:** control-plane, metrics, logging, configuration storage, limited video snippets for forensics/ML:

  * **$200–250 / node / year**.

* **Support & monitoring:**

  * Tier 1/2 support; NOC tooling; incident response; training materials.
  * **$300–350 / node / year**.

* **Tooling & enablement:**

  * Internal dev tools, CI/CD, channel enablement content, partner sandboxes (amortised).
  * **$100–150 / node / year**.

> **Total COGS:** **$600–750 / node / year**.
> At $3,000/node, this implies **gross margin ~75–80%**.

This assumes:

* Most heavy compute runs on **customer/OEM hardware** (edge nodes, NVRs, smart cameras), not our cloud.
* Cloud usage is disciplined and monitored.
* Support is progressively **standardised and automated** (playbooks, dashboards, self-service).

---

## 6. 5-Year US Revenue Scenarios (Node & ARR Only)

Using the node paths in Section 4 and **$3k/node/year**:

### 6.1 Scenario 1 – Conservative (Low Case)

* Nodes: **0.5k → 2k → 6k → 9k → 10–12k**
* ARR: **$1.5M → $6.0M → $18.0M → $27.0M → $30–36M**

This is the “slow but real adoption” path:

* Strong references from a handful of flagship customers.
* Real revenue, but slower SAM penetration; room to grow beyond Year 5.

### 6.2 Scenario 2 – Base (Mid Case)

* Nodes: **1.2k → 4k → 9k → 13k → 15–18k**
* ARR: **$3.6M → $12.0M → $27.0M → $39.0M → $45–54M**

This is the case we consider **most representative of a successful but not insane outcome** in US wedges alone, assuming:

* Healthy but not hyper-growth adoption in transit and logistics.
* 50–60% pilot → rollout conversion.
* GTM capacity ramped sensibly, with partners coming online.

### 6.3 Scenario 3 – Aggressive (High Case)

* Nodes: **2.5k → 8k → 16k → 24k → 25–30k**
* ARR: **$7.5M → $24.0M → $48.0M → $72.0M → $75–90M**

This corresponds to:

* Approaching **full SAM penetration** in wedge verticals plus some lighthouse expansions.
* Very strong references.
* Significant leverage via **SIs and OEMs**.

### 6.4 Margin Profile Across Scenarios

Across all three scenarios:

* We target **GM ~75–80%** as we scale, built on:

  * Node ARR **$3,000**.
  * COGS **$600–750/node/year**.
* Gross profit per node: **$2,250–2,400**.

Our model suggests:

* In **Conservative**, profitability comes later (post-Year 5) unless we keep OPEX extremely tight.
* In **Base**, we can approach **break-even around Year 3** and become solidly profitable in Years 4–5 with healthy EBITDA margins.
* In **Aggressive**, we have headroom to invest more in GTM while still attaining strong overall margins.

(Full FTE/EBITDA breakdown in Appendix E.)

---

## 7. GTM & Vertical Execution

### 7.1 Wedge-Driven Motion (Transit & Logistics)

**Years 1–2 – Pilot-led wedge focus**

* **Transit/Mobility pilots (3–5):**

  * One major metro or commuter agency (platform + vehicle analytics).
  * One bus/BRT system or large city transit operation.
  * One airport rail/shuttle context.

* **Warehousing/Logistics pilots (3–5):**

  * One major 3PL.
  * One e-commerce pure-play.
  * One big-box retailer’s DC network.

Each pilot:

* Deploys **multiple patterns** (at least 3–4) to show breadth:
  restricted-zone intrusion, person-down, crowding/queues, PPE/compliance, equipment misuse.
* Has explicit **before/after metrics**:

  * Investigation time reduction.
  * Additional incidents detected.
  * Operator workload.
  * Any measurable reduction in claims / near-misses (where possible over period).

**Years 3–5 – From pilots to standard playbooks**

* Convert successful pilots into **corridor-level or multi-site rollouts**:

  * Transit: entire corridor/line or fleet segment.
  * Logistics: all DCs in a region, or a set of nationally important DCs.

* Productise into named playbooks, e.g.:

  * **“Rail Safety & Dwell Optimisation Pack”**
    → patterns: restricted-zone, crowding, person-down, aggression.
  * **“Warehouse Safety & Throughput Pack”**
    → patterns: forklift/people conflict, PPE, dock congestion, person-down.

* Grow channel:

  * Train **system integrators** (CCTV, VMS, rail signalling, warehouse automation) to sell and deploy these playbooks.
  * Explore **OEM bundles**: pre-loaded analytics on edge boxes or NVRs.

### 7.2 Long-Term Positioning in the Ecosystem

Longer-term goal:

* Become the **default “safety & ops intelligence layer”** that:

  * Sits **next to** existing VMS/NVR stacks.
  * Consumes camera streams.
  * Emits events/metadata into the customer’s incident & safety workflows.

We do **not** want to replace all VMS; we want:

* SIs and hardware vendors to view us as a **revenue-accretive module**.
* Customers to deploy us **gradually across estates** on their own timelines.

---

## 8. Regulation, Risk & “Why Now”

### 8.1 Safety & Liability Drivers – Warehousing & Logistics

* Warehouses and DCs are among the **highest-risk workplaces**:

  * Forklift and vehicle strikes.
  * Falls from docks and mezzanines.
  * Struck-by or caught-between incidents.

* **Slip/trip/fall and material handling** injuries are major cost drivers for:

  * Workers’ comp claims.
  * OSHA recordables.
  * Lost-time incidents and absenteeism.

* Regulators and insurers increasingly expect:

  * Proactive **hazard identification and mitigation**.
  * Documented evidence that companies are using **“reasonably available technology”** to reduce risk.

### 8.2 Safety & Liability Drivers – Transit / Mobility

* Transit agencies face:

  * Assaults and harassment in vehicles and stations.
  * Vandalism, theft, fare evasion.
  * Suicides and trespass incidents on tracks.
  * Platform crowding and crush risks.

* High-profile incidents lead to:

  * Media scrutiny and political pressure.
  * Regulatory investigations.
  * Civil litigation and settlements.

The question from regulators, boards, and the public increasingly is:

> “What systems did you have in place to **detect and prevent** this?”

### 8.3 Why Edge vs Pure Cloud

**Constraints on “upload everything” approaches:**

* Bandwidth:

  * Vehicles in tunnels or remote depots.
  * Large DCs pushing hundreds of cameras’ worth of video.

* Privacy and policy:

  * Statutes and internal policies limiting off-site/supervisory access to raw video.
  * Unions and worker councils sensitive to “constant remote monitoring”.

**Edge analytics advantages:**

* Raw video remains **on-site**; only events/metadata or short clips are exported.
* Latency is low; reactions to person-down or restricted-zone intrusions can be **seconds**, not minutes.
* Cloud compute costs are controlled; scaling is primarily about **node hardware**.

### 8.4 “Why Now?” in One Sentence

> **Incident and liability pressures are rising, edge compute and models are finally good enough, and organisations are looking for a practical middle ground between dumb cameras and “ship everything to the cloud”.**

---

## 9. Assumptions & Risks (Hypothesis Framing)

This report is a **structured, quantified hypothesis** about a large opportunity—not a forecast locked in stone.

### 9.1 Key Modeling Assumptions

* **Market sizing**:

  * Node TAM **100–190k** (midpoint 150k).
  * SAM **~25–30k nodes** in 5–7 years in US wedges + lighthouses.

* **Pricing**:

  * Effective **$3,000/node/year** realised ARR aligns with ballpark per-camera ranges in adjacent products.

* **Economics**:

  * COGS **$600–750/node/year**; GM **~75–80%** achievable with edge-first compute and disciplined support.

* **Adoption curves**:

  * Conservative/Base/Aggressive paths described in Section 4 are **ambitious but feasible** if:

    * Pilots convert at the suggested rates.
    * We execute GTM and partnerships effectively.

### 9.2 Material Risks

* **Sales cycle risk**:

  * Public transit has long budget cycles and complex procurement.
  * Mitigation: standardised pilot offers, strong SI partners, playbooks that fit into existing RFP structures.

* **Competitive response**:

  * VMS vendors and cloud camera platforms can incrementally add analytics features.
  * Our advantage needs to be:

    * **Edge-centric** rather than cloud-only.
    * **Pattern + playbook IP** rather than generic detectors.
    * Strong integration story with multiple hardware backends.

* **Support and COGS creep**:

  * Heavy bespoke deployments or “special snowflake” integrations could drive up COGS.
  * Mitigation: strict productisation; standard APIs; integration tiers.

* **Regulatory and privacy pushback**:

  * Particularly from unions and worker councils.
  * Mitigation: edge-first design, clear privacy controls, policy templates, and audit logs.

### 9.3 How to Read the Numbers

* Think of all numeric values as **“what we believe is realistic given what we know now”**, not guarantees.
* The key investor-level takeaway is:

> We believe there is a **$75–90M ARR SAM** in our wedges, and we have a **structured, testable plan** to get to **$30–60M ARR** in 5 years in the US if things go reasonably well.

---

## 10. Customer Discovery & Voice of Customer (Plan)

*(Full detail in Appendix F; here is the summary.)*

### 10.1 Interview Plan (15–25 Conversations)

* **Targets by vertical:**

  * **Warehousing & Logistics:**

    * Safety/EHS managers.
    * DC operations managers.
    * Security managers.
    * IT/OT leads.

  * **Transit / Mobility:**

    * Transit safety officers / chiefs.
    * Security / transit police.
    * Operations control centre managers.
    * CIO/IT architects.

  * **Exploratory (expansion):**

    * Retail loss prevention / asset protection.
    * City CCTV program leads.
    * HSE managers in industrial/ports.

* **Volume and timing:**

  * **15–25 interviews** over **3–4 months**, with emphasis on wedges.

### 10.2 Themes & Questions

Key discovery themes:

* Current **incident workflows** (from detection to investigation to remediation).
* Pain points with **video today** (time to find footage, missed incidents).
* Experience with **existing analytics** (basic motion detection, OEM analytics, any AI trials).
* **Budget ownership & procurement paths** (who signs cheques, how decisions are made).
* **Constraints and fears** (IT security, unions, privacy, false positives).
* Perceived **value and ROI** (what would make the solution an obvious “yes”).

### 10.3 Outputs & How They Feed Back

From the first 15–25 interviews, we expect to produce:

* **6–10 anonymised verbatim quotes** capturing key attitudes and pain.
* **1–2 pages of pattern summaries**:

  * Top recurring pains.
  * What they currently do (workarounds).
  * Common objections to AI analytics.
  * Early signals on willingness to pay and preferred pricing models.

This will refine:

* Our **pricing packaging** (per site vs per camera vs per node).
* Our **positioning** (which patterns resonate as “must-have”).
* Our **GTM playbooks** (which roles to target first, how to frame pilots).

---

# Appendices

---

## Appendix A – Competitive Landscape & Alternatives

### A.1 Categories of Alternatives

1. **Traditional VMS + Camera OEM Analytics**

   * Examples: Genetec, Milestone, Avigilon; camera OEM analytics from Axis, Bosch, Hanwha.
   * Strengths:

     * Mature recording/archival & operator workflows.
     * Basic analytics (motion detection, line crossing, simple intrusion, counting).
   * Limitations:

     * Analytics often bolt-on; noisy; configured once, then ignored.
     * Not deeply tied into safety/ops workflows.

2. **Cloud-First Camera/AI Platforms**

   * Examples: Verkada, Meraki, Rhombus, others in cloud camera space.
   * Strengths:

     * Very strong on **ease of deployment**, remote access, updates.
     * Centralised management across many sites.
   * Limitations:

     * Often tied to **proprietary hardware**.
     * Analytics mostly generic (people/vehicle detection, basic counting).
     * Bandwidth and privacy concerns in sensitive environments.

3. **Vertical Safety-AI Startups**

   * Examples:

     * Forklift and PPE safety platforms.
     * Zone-safety analytics for industrial plants.
   * Strengths:

     * Deep focus on one category (forklift-people conflict, PPE).
     * Strong domain knowledge; targeted ROI stories.
   * Limitations:

     * Narrow scope; not a broad platform across verticals.
     * Hardware-locked or bespoke appliances in many cases.

4. **Status Quo / “Do Nothing”**

   * Cameras + NVR + manual review.
   * Occasional motion detection or line-crossing rules that operators largely ignore.

### A.2 Conceptual 2×2

Axes:

* **X-axis:** Generic security / “all-purpose surveillance” ⟶ Deep safety & operations.

* **Y-axis:** Cloud-centric ⟶ Edge-native.

* Traditional VMS/OEM: **generic; more on-prem**, sits **middle-left**.

* Cloud camera platforms: **cloud-centric, generic**; sits **top-left**.

* Vertical Safety-AI startups: **deep but narrow**, often cloud or specific edge; sits **right side** (top/middle).

* **Aixavier:** **edge-native**, **safety/ops-focused**, **pattern/playbook-driven**, sits **bottom-right**.

### A.3 Comparison Table

| Dimension               | Typical VMS                                       | Cloud Camera Platform                           | Vertical Safety-AI Startup                         | **Our Platform (Aixavier)**                                                                                        |
| ----------------------- | ------------------------------------------------- | ----------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Deployment model**    | On-prem server, sometimes hybrid                  | Cloud-first; cameras “phone home”               | Mixed; often custom box or cloud                   | Edge-native runtime + cloud/on-prem control-plane                                                                  |
| **Hardware stance**     | Vendor-agnostic cameras; server HW required       | Often tied to proprietary cameras               | Often tied to specific box/HW                      | Hardware-agnostic runtime (NVIDIA/x86/IPC); optional OEM bundles                                                   |
| **Analytics scope**     | Broad but shallow (motion, line, basic intrusion) | Broad but shallow (people, vehicles, counting)  | Narrow but deep in one domain                      | Broad **pattern catalog**, deep in safety/ops for chosen wedges                                                    |
| **Use-case modelling**  | Individual “features” (tripwire, count)           | Basic detectors and alerts                      | Concrete single-purpose scenarios (PPE, forklifts) | **Pattern-based playbooks** (restricted zones, person-down, crowding, aggression, etc.), parameterised by vertical |
| **Customisability**     | Rules/layouts; deeper changes = PS projects       | Configurable in cloud UI; limited model control | Limited beyond core scenarios                      | Configurable patterns and rules; vertical templates; PS used to extend catalog                                     |
| **Integration style**   | SDKs, plugins for VMS, on-prem APIs               | Cloud/webhooks; some on-prem agents             | Often bespoke integration                          | Designed to sit **next to existing VMS/NVR**, with standard event/metadata APIs                                    |
| **Cloud vs Edge**       | Mostly on-prem; some hybrid                       | Cloud-heavy; video often leaves site            | Varies by vendor                                   | Edge-heavy inference; cloud for fleet management & metrics                                                         |
| **Typical positioning** | Core “video plumbing”                             | All-in-one cloud camera stack                   | Single-domain safety add-on                        | Cross-vertical **safety/ops intelligence layer** on existing camera+VMS                                            |

**Explicit acknowledgement:**
Many incumbents already have **zone intrusion, counting, and dwell-time analytics** as checkboxes. Our differentiation is **not** “we detect objects too”, but:

* **Edge-native design** tailored to bandwidth/privacy constraints.
* A **pattern + playbook catalog** focused on safety & ops outcomes.
* Deliberate **multi-backend** integration strategy with existing camera+VMS ecosystems.

---

## Appendix B – Existing Edge & VMS Ecosystem (Transit & Warehousing)

### B.1 Transit / Mobility Stack

Common components:

* **Cameras:** IP (Axis, Bosch, Hanwha, Panasonic, etc.), vehicle-rated models, some analog on older systems.
* **Vehicle recorders / mobile NVRs:** dedicated boxes with SSD/HDD, often vendor-specific.
* **Station VMS:** Genetec, Milestone, Avigilon, OnSSI, etc., deployed per station or centrally.
* **Backhaul:** wired networks in stations; Wi-Fi/cellular backhaul for vehicles.

Deployment options for Aixavier:

1. **Agent/container on existing edge servers/NVRs**

   * Where NVRs or station servers support containers or third-party services.
   * Pros: no extra hardware, simpler procurement.
   * Cons: heterogeneous platforms; varying performance.

2. **Separate edge appliance**

   * Dedicated box in rack rooms or vehicle cabinets.
   * Taps RTSP/ONVIF streams from cameras/NVRs.
   * Sends events/metadata back to VMS and incident systems.

**Integration priorities:**

* Target VMS vendors with open APIs/event injection.
* Mobile NVR vendors that:

  * Expose streams.
  * Allow light-weight apps or send metadata.

### B.2 Warehousing & Logistics Stack

Components:

* **Cameras:** IP cameras from common OEMs; legacy analog via encoders.
* **NVRs:** off-the-shelf NVRs or VMS-managed storage servers.
* **VMS:** mid-market to enterprise-grade, depending on operator size.
* **Network:** wired inside facility; some separate OT or security subnets.

Deployment options:

1. **Service on existing x86/NVR/industrial PC**

   * When the environment supports Windows/Linux services or containers.
   * Minimises new hardware; good for enterprises standardised on a vendor.

2. **Dedicated edge appliance**

   * In the network rack, ingesting streams from cameras/NVRs.
   * Publishes events into VMS/SOC dashboards and safety tools.

**Logical partnerships:**

* VMS vendors strong in **logistics/industrial** verticals.
* NVR/industrial PC vendors already selling into DCs.
* Automation integrators (WMS, robotics) who want to bundle safety analytics.

---

## Appendix C – Buying Journey & GTM Details

### C.1 Warehousing & Logistics – Buying Journey

* **Champion:**

  * Safety/EHS manager, or
  * DC operations manager who owns throughput and injuries.

* **Economic buyer:**

  * VP Operations, Head of Supply Chain.
  * Sometimes CFO if claims are large and visible.

* **Gatekeepers:**

  * IT (network, security, architecture).
  * Legal/Risk (privacy, policies).
  * EHS if not champion.

* **Sales path:**

  * Early: **direct + a few trusted integrators**, pilot-heavy.
  * Later: via **existing integrators** who already supply CCTV/WMS/automation.

### C.2 Transit / Mobility – Buying Journey

* **Champion:**

  * Chief safety officer or equivalent.
  * Security lead / transit police.
  * Operations control centre leadership.

* **Economic buyer:**

  * COO / Director of Operations.
  * Sometimes CIO/CTO if embedded into broader modernisation.

* **Gatekeepers:**

  * IT (cybersecurity, integration).
  * Legal/compliance.
  * Unions / worker councils (privacy & real-time monitoring concerns).

* **Sales path:**

  * Early: **direct engagement + pilots**, usually with a specialised transit SI.
  * Later: part of bigger **SI/OEM contracts** (rolling stock upgrades, signalling, control room projects).

### C.3 GTM Evolution

* **Years 1–2:** founder-led, direct sales; design partner style pilots.
* **Years 3–5:** shift towards **SI and OEM-driven distribution**; playbooks packaged for resale.
* **Long-term:** analytics becomes a **standard line item/module** in transit and DC solution stacks.

---

## Appendix D – Canonical Pattern Table (Detailed)

| Pattern                              | Short Description                    | Transit / Mobility Example                                | Warehousing / Logistics Example                                                  |
| ------------------------------------ | ------------------------------------ | --------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Restricted-zone intrusion            | Entry into defined no-go zone        | Passenger steps beyond platform edge; trespass in tunnel  | Worker enters forklift-only aisle; person in exclusion zone near heavy machinery |
| Unattended / suspicious object       | Object left unmoved beyond threshold | Luggage left near stairs/gate for >X minutes              | Pallet left blocking fire exit; object in emergency pathway                      |
| Person-down / fall / collapse        | Human falls or lies motionless       | Passenger collapses in railcar or on platform             | Worker falls off dock; person lying on warehouse floor                           |
| Crowding / over-capacity / queues    | Density or queues exceed limit       | Platform overcrowded; entrance blocked; dwell extended    | Long checkout/staging queues; congested dock or lane                             |
| Aggression / violence / fighting     | Patterns suggesting fight/assault    | Two people fighting inside train or at station            | Physical altercation in break area or yard                                       |
| Staff compliance & presence          | Staff/PPE vs expected rules          | No staff at assigned door during dwell                    | Worker in high-risk area without PPE; no spotter where required                  |
| Equipment misuse / unsafe operation  | Machine outside safe envelope        | Doors forced while train moving; riding outside safe area | Forklift speeding; elevated load near pedestrians; riding on forks               |
| Environmental & smoke/fire anomalies | Smoke, haze, flame anomalies         | Smoke in car; bin fire on platform                        | Smoke near battery racks; haze in hazardous storage zone                         |

**Usage:**

* Each pattern is implemented once, then **parameterised by vertical** (zones, thresholds, semantics).
* New verticals map to the same patterns; we **don’t** reinvent new detectors each time.

---

## Appendix E – Financial Appendix (FTE & EBITDA Sketch)

### E.1 FTE Ramp (Illustrative, Base Case)

* **Y1:** ~20 FTE

  * Founders, core engineering (models + runtime), 1 PM, 1–2 sales, 1 ops/support.
* **Y2:** ~35 FTE

  * More engineers (deployment + integrations), 2–3 GTM hires, 1–2 support/CS.
* **Y3:** ~55 FTE

  * Dedicated vertical PMs, more AE/SE headcount, customer success, support.
* **Y4:** ~75 FTE

  * Regional GTM coverage, partner managers, reliability and SRE.
* **Y5:** ~95 FTE

  * Mature GTM and eng teams; expanded CS and partner enablement.

**Blended fully-loaded cost:**
We use **$180k/FTE/year** as a modelling assumption (US-weighted, some global hiring).

### E.2 EBITDA Trajectory (Qualitative)

Given:

* Node/ARR scenarios (Section 6).
* GM target **75–80%**.
* FTE ramp above, plus **15–20% of revenue** as other OPEX (marketing, travel, G&A).

We get:

* **Conservative (low case):**

  * Y1–Y2: meaningfully negative EBITDA while building product and references.
  * Y3: narrower losses as revenue increases.
  * Y4–Y5: approaching break-even to modest profitability.

* **Base (mid case):**

  * Y1: negative, heavy investment.
  * Y2: losses shrink as ARR grows.
  * **Y3:** near break-even.
  * **Y4–Y5:** opportunity for **20–30%+ EBITDA margin** if growth and efficiency are balanced.

* **Aggressive (high case):**

  * We may **reinvest** aggressively in GTM and R&D; profitability depends on pace of hiring.
  * Even with investment, the underlying economics support attractive margins at scale.

(Investors can reconstruct exact numbers from nodes × pricing, COGS assumption, FTE ramp, and OPEX %.)

---

## Appendix F – Customer Discovery & Research Roadmap (Detailed)

### F.1 Customer Interviews – Detailed Plan

**Roles per vertical:**

* **Warehousing & Logistics:**

  * Safety/EHS.
  * DC Ops / Site Manager.
  * Security.
  * IT/OT.

* **Transit / Mobility:**

  * Safety officer.
  * Security / transit police.
  * OCC manager.
  * CIO/IT architect.

* **Exploratory (expansion):**

  * Retail LP/AP.
  * City CCTV programme managers.
  * Industrial HSE.

**Volumes:**

* 8–12 interviews in warehousing & logistics.
* 6–8 in transit/mobility.
* 3–5 exploratory.

### F.2 Interview Guide – Sample Questions

**Incident workflow**

* “Tell me about the last serious safety incident. How did you find out, and how did video get used?”
* “How long did it take to locate and review the relevant footage?”

**Pain with video**

* “Where does video fail you today?”
* “Do you feel like you’re missing incidents?”

**Analytics experience**

* “What analytics do you have now (if any)? Motion, lines, AI? Do you trust them?”
* “Have you trialed advanced analytics before? What happened?”

**Budgets & procurement**

* “Who would sign a cheque for a system like this?”
* “Which budget does it come from (Safety, Security, Ops, IT, CapEx/OpEx)?”
* “How do you normally buy tech like this? RFP, pilots, multi-year contracts?”

**Constraints/fears**

* “What would make you nervous about ‘AI watching cameras’?”
* “If a vendor promised ‘zero false positives’, what would you think?”

**Value & ROI**

* “If this worked extremely well, what would it change in 12–24 months?”
* “What evidence would you need to see to say: this is obviously worth paying for?”

### F.3 Expected Outputs – Example Quotes & Patterns

Once we’ve run a first tranche, we expect to summarise:

**Example anonymised quotes:**

* > “We have 900+ cameras and maybe three pairs of eyes watching them. Most of the time we’re blind until someone gets hurt.” – Ops Manager, large DC
* > “After an incident, we spend days scrubbing video. The worst part is when we never find the one moment that matters.” – Safety Lead, commuter rail
* > “We’ve tried AI analytics, but false positives killed it. Once my team stops trusting alerts, the system is dead.” – Security Manager, warehouse campus
* > “Our IT folks don’t want any live video streaming to the cloud. If it doesn’t run on-site, it’s basically a non-starter.” – IT Architect, transit agency

**Patterns:**

* Investigation time is **too long**; staff time is expensive.
* Many incidents are missed **entirely** because no one is watching.
* Distrust of generic “AI analytics” due to false positives.
* Strong concern about **privacy, bandwidth, security** and cloud.

### F.4 Research Roadmap (3–12 Months)

**Data to collect:**

* **Customer interviews** (above).

* **Pilot metrics**:

  * Per pattern: precision/recall, FP/FN rates.
  * Investigation time before/after.
  * Any measured change in incident detection or near-miss capture.

* **Integration friction**:

  * Document how hard each VMS/NVR stack is to integrate with.
  * Build qualitative “integration difficulty scores”.

* **Pricing experiments**:

  * Compare response to per-node vs per-site vs per-camera quotes.
  * Observe discount sensitivity and preferred term lengths.

* **Cost actuals vs model**:

  * Track real **cloud and support costs** per node in pilots.
  * Compare to **$600–750/node/year** assumption.

This roadmap ensures the model in this memo becomes **tighter and more evidence-backed** over the next **3–12 months**.