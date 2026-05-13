"""AETHER OS CLI v2 - Con Training Agent."""

import asyncio
from aether_os.core_v2 import AetherCoreV2
from aether_os.agents.training_agent import TrainingAgent
from aether_os.saas_division import SaaSDivision


class AetherOSCLI:
    """CLI profesional para AETHER OS."""
    
    def __init__(self):
        self.core = AetherCoreV2()
        self.trainer = TrainingAgent()
        self.saas = SaaSDivision()
    
    async def main_menu(self):
        """Menú principal."""
        
        print("\n" + "="*70)
        print("AETHER OS v2.0 - CLI PROFESIONAL")
        print("="*70 + "\n")
        
        while True:
            print("OPCIONES:")
            print("1. Generar TODO App")
            print("2. Entrenar Agente")
            print("3. Ver Metricas")
            print("4. Salir\n")
            
            choice = input("Elige (1-4): ").strip()
            
            if choice == "1":
                await self.generate_saas()
            elif choice == "2":
                await self.train_agent()
            elif choice == "3":
                self.show_metrics()
            elif choice == "4":
                print("\nHasta luego!\n")
                break
            else:
                print("Opcion invalida\n")
    
    async def generate_saas(self):
        print("\nGenerando TODO App...")
        result = await self.saas.create_todo_app()
        print(f"Completado: {result['tasks']} tareas\n")
    
    async def train_agent(self):
        agent = input("\nNombre del agente: ").strip()
        logs = [
            {"status": "completed", "tokens": 4500},
            {"status": "completed", "tokens": 4200},
            {"status": "failed", "tokens": 5000},
        ]
        print(f"\nEntrenando {agent}...")
        result = await self.trainer.train_agent(agent, logs)
        rate = result['initial_success_rate']
        print(f"Tasa inicial: {rate:.1f}%\n")
    
    def show_metrics(self):
        metrics = self.core.metrics.get_report()
        print("\n" + "="*70)
        print("METRICAS DEL SISTEMA")
        print("="*70)
        print(f"Tareas: {metrics['tasks_executed']}")
        print(f"Fallos: {metrics['tasks_failed']}")
        print(f"Tokens: {metrics['total_tokens']}")
        cost = metrics['total_cost']
        print(f"Costo: {cost:.4f} USD")
        print(f"Exito: {metrics['success_rate']:.1f}%\n")


async def main():
    cli = AetherOSCLI()
    await cli.main_menu()


if __name__ == "__main__":
    asyncio.run(main())
