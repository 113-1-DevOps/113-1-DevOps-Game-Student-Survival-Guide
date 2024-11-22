import pygame
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.controllers.game_controller import *

# OpenTelemetry 導入
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# 配置 OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# 配置 OTLP Exporter，將數據發送到 OpenTelemetry Collector
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

def start():
    with tracer.start_as_current_span("game_initialization"):
        pygame.init()
        controller = GameController()

    running = True
    with tracer.start_as_current_span("game_loop") as span:
        while running:
            for event in pygame.event.get():
                # 記錄事件處理
                with tracer.start_as_current_span("event_handling") as event_span:
                    if event.type == pygame.QUIT:
                        running = False
                        event_span.set_attribute("event.type", "QUIT")
                    else:
                        event_span.set_attribute("event.type", str(event.type))
                        with tracer.start_as_current_span("controller_handle_event"):
                            controller.handle_event(event)

if __name__ == '__main__':
    # 主執行邏輯
    try:
        with tracer.start_as_current_span("main_execution"):
            start()
    except Exception as e:
        with tracer.start_as_current_span("error") as error_span:
            error_span.record_exception(e)
            print(f"Error occurred: {e}")
