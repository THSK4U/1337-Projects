from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataStream(ABC):
    def __init__(self, stream_id: str = None,
                 type_str: str = None, batch: List[Any] = None) -> None:
        self.stream_id = stream_id
        self.type_str = type_str
        self.batch = batch

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        if not criteria:
            return data_batch

        filter_data = [data for data in data_batch if data == criteria]
        return filter_data

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        len_self = len(self.batch)
        return {f"{self.stream_id}": len_self}


class SensorStream(DataStream):
    def __init__(self, stream_id: str = None,
                 type_str: str = None, batch: List[Any] = None) -> None:
        super().__init__(stream_id, type_str, batch)

    def process_batch(self, data_batch: List[Any]) -> str:
        data_list: list[str] = []
        temps: List[int] = []
        try:
            for data in data_batch:
                if isinstance(data, dict):
                    for key, value in data.items():
                        data_list.append(f"{key}:{value}")
                        if key == "temp":
                            temps.append(value)

            avg_temp: float = sum(temps) / len(temps)
            return f"""Stream ID: {self.stream_id}, Type: {self.type_str}
Processing sensor batch: [{', '.join(data_list)}]
Sensor analysis: {len(data_batch)} readings processed, avg temp: \
{avg_temp}°C"""
        except Exception as e:
            return f"Error: {str(e)}"

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        len_self = len(self.batch)
        return {"Sensor": f"{len_self} readings"}

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        if not criteria:
            return data_batch
        filter_data = [data for data in data_batch
                       if data.get("humidity", 0) > 55
                       or data.get("pressure", 0) > 1000]
        return filter_data


class TransactionStream(DataStream):
    def __init__(self, stream_id: str = None,
                 type_str: str = None, batch: List[Any] = None) -> None:
        super().__init__(stream_id, type_str, batch)

    def process_batch(self, data_batch: List[Any]) -> str:
        data_list: list[str] = []
        units: int = 0
        try:
            for data in data_batch:
                if isinstance(data, dict):
                    for key, value in data.items():
                        data_list.append(f"{key}:{value}")

                        if key == "buy":
                            units += value
                        elif key == "sell":
                            units -= value

            return f"""Stream ID: {self.stream_id}, Type: {self.type_str}
Processing transaction batch: [{', '.join(data_list)}]
Transaction analysis: {len(data_batch)} operations, net flow: +{units} units"""
        except Exception as e:
            return f"Error: {str(e)}"

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        len_self = len(self.batch)
        return {"Transaction": f"{len_self} operations"}

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        if not criteria:
            return data_batch
        filter_data = [data for data in data_batch if data.get("buy", 0) > 100
                       or data.get("sell", 0) > 100]
        return filter_data


class EventStream(DataStream):
    def __init__(self, stream_id: str = None,
                 type_str: str = None, batch: List[Any] = None) -> None:
        super().__init__(stream_id, type_str, batch)

    def process_batch(self, data_batch: List[Any]) -> str:
        data_list: list[str] = []
        len_error: int = 0
        try:
            for data in data_batch:
                if isinstance(data, str):
                    data_list.append(f"{data}")
                if data == "error":
                    len_error += 1
            return f"""Stream ID: {self.stream_id}, Type: {self.type_str}
Processing event batch: [{', '.join(data_list)}]
Event analysis: {len(data_batch)} events, {len_error} error detected"""
        except Exception as e:
            return f"Error: {str(e)}"

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        len_self = len(self.batch)
        return {"Event": f"{len_self} events"}


class StreamProcessor:
    def __init__(self, streams: List[Any]):
        self.streams = streams

    def stream_processing(self):
        print("""Processing mixed stream types through unified interface...

Batch 1 Results:""")
        for stream in self.streams:
            stats = stream.get_stats()
            for key, value in stats.items():
                print(f"- {key} data: {value} processed")

    def stream_filter(self, criteria: str) -> None:
        results: List[str] = []
        for stream in self.streams:
            filter_data = stream.filter_data(stream.batch, criteria)

            count = len(filter_data)

            if (count > 0):
                if isinstance(stream, SensorStream):
                    desc = "critical sensor alerts"
                elif isinstance(stream, TransactionStream):
                    desc = "large transaction"

                results.append(f"{count} {desc}")

        print(f"Filtered results: {','.join(results)}")


def main():
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

    print("\nInitializing Sensor Stream...")
    sensor_obj = SensorStream("SENSOR_001", "Environmental Data",
                              [{"temp": 22.5},
                               {"humidity": 65},
                               {"pressure": 1013}])
    print(sensor_obj.process_batch(sensor_obj.batch))

    print("\nInitializing Transaction Stream...")
    trans_obj = TransactionStream("TRANS_001", "Financial Data",
                                  [{"buy": 100},
                                   {"sell": 150},
                                   {"buy": 75}])
    print(trans_obj.process_batch(trans_obj.batch))

    print("\nInitializing Event Stream...")
    event_obj = EventStream("EVENT_001", "System Events",
                            ["login", "error", "logout"])
    print(event_obj.process_batch(event_obj.batch))

    print("\n=== Polymorphic Stream Processing ===")

    stream_obj = StreamProcessor([sensor_obj, trans_obj, event_obj])
    stream_obj.stream_processing()

    criteria = "High-priority"
    print(f"\nStream filtering active: {criteria} data only")
    stream_obj.stream_filter(criteria)

    print("\nAll streams processed successfully. Nexus throughput optimal.")


main()
