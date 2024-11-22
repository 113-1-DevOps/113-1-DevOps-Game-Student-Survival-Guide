import pygame
import os, sys

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

    pygame.init()
    controller = GameController()
    
    clock = pygame.time.Clock()
     
    running = True
    try:
        while running:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    controller.handle_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    controller.handle_event(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    controller.handle_event(event)
                elif event.type == pygame.MOUSEMOTION:
                    controller.handle_event(event)
                else:
                    continue
                    
            pygame.display.flip()
            clock.tick(60)
    except Exception as e:
        print("An unexpected error occurred: %s", e)
                    
if __name__ == '__main__':
    start()
