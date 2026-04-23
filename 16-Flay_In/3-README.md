*This project has been created as part of the 42 curriculum by tsellak.*

# Fly-in: Drones are interesting

## Description

The "Fly-in" project involves simulating and optimizing the flight paths of a fleet of drones through a complex network of zones. The primary goal is to route these drones from a starting zone to an end zone in the minimum number of turns while strictly respecting zone capacities, connection limits, and specific movement constraints (e.g., navigating around restricted or blocked zones).

## Instructions

Ensure that you have Python 3 installed. The project handles its dependencies via `requirements.txt` / `uv`.

```bash
# Setup virtual environment (Optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (if any)
pip install -r requirements.txt

# Run the simulation on a test map
python3 main.py maps/easy_map.txt
```

## Algorithm Choices & Implementation Strategy

The project relies on multiple graph traversal techniques implemented in the `pathfinding.py` file to find optimal paths over the drone network:

- **Dijkstra's Algorithm (`find_path`)**: Used to find the shortest and most cost-effective path between zones. It maps out paths while accounting for different zone weights (e.g., restricted zones have a higher cost/weight).
- **Depth-First Search (`get_all_paths`)**: A recursive DFS approach is used to explore all possible routes from start to finish. This is essential for calculating flow capacities (`compute_flows`) and distributing multiple drones over parallel paths to avoid congestion.
- **Simulation (`simulation.py`)**: Executes the computed paths turn-by-turn. It properly formats the output as required (e.g., `D1-roof1 D2-corridorA`) and triggers the visualizer.

## Visual Representation

A graphical visualizer (`visualization.py`) runs at the end of the simulation. It provides a visual representation of the network (Zones and Connections) and animates the drones as they move along their paths. This strongly enhances the user experience and helps debug complex map topologies by instantly revealing bottlenecks.

## Resources

- **Reference Material**:
  - Graph Theory, specifically Dijkstra's and DFS algorithms.
  - Network Flow principles (understanding link capacities and zone bottlenecks).
- **AI Usage**:
  - AI tools were used to help document the algorithms, clarify graph theory concepts, and structure this README.

---

<div dir="rtl">

## المفاهيم والمصطلحات البرمجية التي يجب تعلمها (Learning Concepts)

### 1. خوارزمية ديكسترا (Dijkstra's Algorithm)

**ماذا:**

- خوارزمية تُستخدم لإيجاد أقصر مسار بين نقطة البداية وأي نقطة أخرى في الرسم البياني (Graph).

**لماذا:**

- لأن خريطة الطائرات بدون طيار تحتوي على مناطق ذات تكلفة مختلفة (مثل `restricted zones` التي تستهلك وقتاً أطول).
- نحتاج للخوارزمية لضمان وصول الطائرات بأقل عدد ممكن من الخطوات (Turns) لتجنب الازدحام.

**كيف:**

- تعمل عن طريق تفقد جميع النقاط المجاورة، واختيار النقطة ذات التكلفة المتراكمة الأقل للتقدم.
- في الكود (دالة `find_path`)، تم استخدام قائمة كمخزن لتتبع المسافات (Distances)، وفي كل خطوة يتم زيارة المنطقة الأقرب وتحديث مسافات جيرانها.

### 2. البحث في العمق (Depth-First Search - DFS)

**ماذا:**

- خوارزمية للتوغل في الرسوم البيانية تعتمد على المشي في مسار معين حتى أعمق نقطة، ثم التراجع (Backtracking) عند الوصول لطريق مسدود.

**لماذا:**

- مفيدة لاستكشاف جميع المسارات المتاحة من البداية إلى النهاية لتقييمها (تم استخدامها في الدالة `get_all_paths`).
- تساعد في إيجاد مسارات بديلة لتوزيع الطائرات في حالة كانت السعة (Capacity) لأقصر مسار غير كافية لجميع الطائرات.

**كيف:**

- تبدأ الخوارزمية من نقطة البداية (Start Zone) وتنتقل إلى أول جار، ثم تستمر بالتقدم حتى تجد نقطة النهاية (End Zone) أو طريقاً مسدوداً.
- عند التراجع، تستكشف المسار المتاح التالي وتضيفه إلى قائمة كل المسارات المحتملة.

### 3. الرسوم البيانية (Graphs / Nodes & Edges)

**ماذا:**

- هيكل بيانات برمجي وتقنية رياضية تتكون من "عقد" (Nodes) تمثل المناطق (Zones)، و"روابط" (Edges) تمثل الاتصالات (Connections) بينها.

**لماذا:**

- لأن خريطة العالم الخاصة بالمشروع (Fly-in) ليست مصفوفة بسيطة (Grid)، بل شبكة معقدة من الأماكن التي ترتبط ببعضها بسعات تدفق (Flow Capacities) مختلفة.

**كيف:**

- في الكود (`models.py`)، تُستخدم الكائنات (Objects) لتمثيلها: الفئة `Zone` هي العقدة، والفئة `Connection` هي الرابط.
- نقوم بتحويل هذه الكائنات إلى رسم بياني في `pathfinding.py` لكي تتمكن الخوارزميات من حساب عدد الطائرات (`max_drones` و `max_link_capacity`) التي يمكنها العبور بأمان.

</div>
