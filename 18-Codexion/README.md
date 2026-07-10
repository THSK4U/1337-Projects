*This project has been created as part of the 42 curriculum by tsellak.*

## Description

Codexion is a multi-threaded simulation in which coders work in a shared environment with limited hardware resources (dongles). Each coder must acquire two dongles to perform a compilation cycle, which consists of compiling, debugging, and refactoring. The simulation must address concurrency issues, such as preventing deadlocks and starvation, managing resource cooldown periods, precisely detecting burnout, and ensuring thread-safe logging.

The goal is to implement a robust concurrent system in which multiple coder threads compete for shared dongle resources, and a monitor thread detects burnout conditions. The simulation ends when all the coders have completed their required compilations or when a coder burns out (when they exceed their time-to-burnout deadline).

## Instructions

### Compilation

```bash
make
```

This produces the `codexion` executable.

### Execution

```bash
./codexion <number_of_coders> <time_to_burnout> <time_to_compile> <time_to_debug> <time_to_refactor> <number_of_compiles_required> <dongle_cooldown> <scheduler>
```

**Arguments:**
- `number_of_coders`: Number of coder threads (and dongles) — positive integer
- `time_to_burnout`: Time in milliseconds before a coder burns out — positive integer
- `time_to_compile`: Compilation duration in milliseconds — positive integer
- `time_to_debug`: Debugging duration in milliseconds — positive integer
- `time_to_refactor`: Refactoring duration in milliseconds — positive integer
- `number_of_compiles_required`: Number of compilation cycles each coder must complete — positive integer
- `dongle_cooldown`: Cooldown period in milliseconds after releasing a dongle — positive integer
- `scheduler`: Scheduling algorithm — `fifo` (First-In-First-Out) or `edf` (Earliest Deadline First)

**Example:**
```bash
./codexion 5 800 200 100 100 7 50 edf
```

### Cleanup

```bash
make clean      # Remove object files
make fclean     # Remove object files and executable
make re         # Rebuild from scratch
```

## Resources

- **POSIX Threads (pthreads)**: `man pthreads`, `man pthread_mutex_lock`, `man pthread_cond_wait`
- **Dining Philosophers Problem**: Classic concurrency problem — this project is a variation with deadlines
- **Earliest Deadline First (EDF) Scheduling**: Real-time scheduling algorithm
- **Deadlock Prevention**: Resource ordering, Coffman conditions avoidance

### AI Usage

AI was used for:
- Generating this README.md from the source code analysis
- Explaining complex concurrency concepts (deadlock prevention, EDF scheduling)
- Code review suggestions for thread safety improvements

## Blocking Cases Handled

### Deadlock Prevention (Coffman's Conditions)

The implementation addresses all four Coffman conditions to prevent deadlock:

1. **Mutual Exclusion**: Each dongle is protected by a `pthread_mutex_t` — only one coder can hold a dongle at a time.
2. **Hold and Wait**: Avoided by acquiring dongles in a strict global order (always lower ID first). In `take_two_dongles()` (dongle.c:50-74), dongles are sorted by ID before acquisition. If the second dongle cannot be acquired, the first is released immediately.
3. **No Preemption**: Dongles are not preempted, but the ordered acquisition eliminates circular wait.
4. **Circular Wait**: Eliminated by the global ordering — all coders acquire dongles in increasing ID order, making circular wait impossible.

### Starvation Prevention

Two scheduling policies are implemented:

- **FIFO (First-In-First-Out)**: Coders are queued in arrival order. The first coder to request a dongle gets it first.
- **EDF (Earliest Deadline First)**: Coders with earlier burnout deadlines get priority. Implemented as a min-heap on each dongle's queue (`heap.c`), comparing `deadline` then `id` as tiebreaker.

The heap ensures O(log n) insertion and extraction while maintaining priority order.

### Cooldown Handling

After releasing a dongle (`release_one_dongle()`, dongle.c:38-48), the dongle enters a cooldown period (`dongle_cooldown` ms). During this time:
- The dongle's `release_time` is set to current time + cooldown
- Other coders waiting on that dongle will block until cooldown expires
- The condition variable is broadcast to wake waiters when cooldown ends

### Precise Burnout Detection

The monitor thread (`monitor_routine()`, monitor.c:50-66) runs a continuous loop:
- Checks all coders every 1ms (`usleep(1000)`)
- Compares current time against each coder's `deadline` (set at compile start)
- If `now >= deadline`, calls `mark_burnout()` which atomically sets `simulation_end` and logs the event
- Also terminates when all coders complete required compilations (`check_and_mark()`)

The `sleep_until_or_burnout()` function (time_utils.c:31-48) allows coders to sleep during phases while checking for burnout at fine granularity (10ms or 1ms intervals).

### Log Serialization

All logging goes through `log_action()` (logger.c:9-17) which:
- Locks `print_mutex` before printing
- Outputs: `<timestamp> <coder_id> <message>`
- Unlocks `print_mutex` after printing

This ensures log lines are never interleaved.

## Thread Synchronization Mechanisms

### Mutexes

| Mutex | Purpose | Location |
|-------|---------|----------|
| `dongle.mutex` | Protects dongle state (`in_use`, `release_time`, queue) | codexion.h:25 |
| `data.print_mutex` | Serializes log output | codexion.h:48 |
| `data.state_mutex` | Protects `simulation_end` flag | codexion.h:49 |

### Condition Variables

| Condition Variable | Purpose | Location |
|-------------------|---------|----------|
| `dongle.cond` | Wait/notify for dongle availability and cooldown expiry | codexion.h:26 |

### Race Condition Prevention Examples

**Dongle Acquisition** (dongle.c:12-36):
```c
pthread_mutex_lock(&dongle->mutex);
queue_push(dongle, coder);  // Enqueue under lock
while (dongle->in_use || get_time_ms() < dongle->release_time
       || dongle->queue[0] != coder) {
    // Check burnout under same lock
    if (get_time_ms() >= coder->deadline || simulation_check(...))
        return (fail_take(dongle, coder));
    ms_to_timespec(&ts, get_next_timeout(coder, dongle));
    pthread_cond_timedwait(&dongle->cond, &dongle->mutex, &ts);
}
queue_pop(dongle, coder->data);  // Dequeue under lock
dongle->in_use = 1;
pthread_mutex_unlock(&dongle->mutex);
```

All state checks and modifications happen under the dongle's mutex. The condition variable wait is atomic with the mutex release/reacquire.

**Monitor-Coder Communication** (monitor.c:28-48, time_utils.c:31-48):
- `simulation_end` flag protected by `state_mutex`
- `simulation_check()` reads the flag under lock
- `mark_burnout()` writes the flag under lock
- Coders check `simulation_check()` during sleeps and dongle waits

**Log Serialization** (logger.c:9-17):
```c
pthread_mutex_lock(&coder->data->print_mutex);
printf("%ld %d %s\n", time_now, coder->id, message);
pthread_mutex_unlock(&coder->data->print_mutex);
```

Single mutex ensures atomic log lines from all threads.

### Thread-Safe Communication Between Coders and Monitor

1. **Burnout Detection**: Monitor reads `coder->deadline` (set by coder under no lock, but only written once at compile start) and current time. If deadline passed, monitor calls `mark_burnout()` which atomically sets `simulation_end=1` under `state_mutex`.

2. **Simulation Termination**: Coders call `simulation_check()` (monitor.c:4-12) which reads `simulation_end` under `state_mutex`. Returns true if simulation should end.

3. **Dongle Wait with Timeout**: `get_next_timeout()` (time_utils.c:18-29) computes minimum of coder's deadline and dongle's cooldown expiry. `pthread_cond_timedwait` wakes at the earlier of the two, allowing coder to re-check both conditions.

## Technical Choices

- **Global Dongle Ordering**: Always acquire lower-ID dongle first to prevent circular wait
- **Per-Dongle Queue + Heap**: Each dongle maintains its own wait queue; EDF uses binary min-heap for O(log n) priority operations
- **Timed Condition Wait**: `pthread_cond_timedwait` with dynamic timeout allows responsive burnout detection during dongle wait
- **Fine-Grained Sleep with Checks**: `sleep_until_or_burnout` uses 10ms/1ms sleeps with periodic burnout/end checks instead of single long sleep
- **Separate Mutexes**: Print and state mutexes are separate from dongle mutexes to minimize contention
