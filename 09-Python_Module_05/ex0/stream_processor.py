from typing import Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):

    silent_mode: bool = False

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        try:
            if not super().silent_mode:
                print(f"Processing data: {data}")
            if not self.validate(data):
                raise
            len_dt: int = len(data)
            sum_num: float = sum(data)
            return f"Processed {len_dt} numeric values,"\
                f" sum={sum_num}, avg={sum_num/len_dt}"
        except Exception:
            return "ERROR: Data not verified numeric values"

    def validate(self, data: Any) -> bool:
        for dt in data:
            try:
                try:
                    int(dt)
                except Exception:
                    float(dt)
            except Exception:
                return False
        if not super().silent_mode:
            print("Validation: Numeric data verified")
        return True


class TextProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        if not super().silent_mode:
            print(f"Processing data: \"{data}\"")
        if not self.validate(data):
            return "ERROR: Data not verified Text"
        count_words: list[str] = list(data.split(' '))
        return f"Processed text: {len(data)} characters, \
{len(count_words)} words"

    def validate(self, data: Any) -> bool:
        if type(data) is not str:
            return False
        if not super().silent_mode:
            print("Validation: Text data verified")
        return True


class LogProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        if not super().silent_mode:
            print(f"Processing data: \"{data}\"")
        if not self.validate(data):
            return "ERROR: Data not verified Log"
        neo_data: list[str] = data.split(':')
        if "ERROR" == neo_data[0]:
            mode = "ALERT"
        else:
            mode = neo_data[0]
        return f"[{mode}] {neo_data[0]} level detected:{neo_data[1]}"

    def validate(self, data: Any) -> bool:
        if type(data) is not str or ':' not in data:
            return False
        if not super().silent_mode:
            print("Validation: Log entry verified")
        return True


def main() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")

    print("\nInitializing Numeric Processor...")
    N_P = NumericProcessor()
    print(N_P.format_output(N_P.process([1, 2, 3, 4, 5])))

    print("\nInitializing Text Processor...")
    T_P = TextProcessor()
    print(T_P.format_output(T_P.process("Hello Nexus World")))

    print("\nInitializing Log Processor...")
    L_P = LogProcessor()
    print(L_P.format_output(L_P.process("ERROR: Connection timeout")))

    print("\n=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")

    DataProcessor.silent_mode = True

    list_P: list[DataProcessor] = [N_P, T_P, L_P]
    list_data: list[Any] = [[1, 2, 3], "hello world!", "INFO: system ready"]
    for i in range(3):
        print(f"Result {i}: {list_P[i].process(list_data[i])}")

    print("\nFoundation systems online. Nexus ready for advanced streams")


main()
