"""AETHER OS CLI - Interfaz por línea de comandos."""

import asyncio
from aether_os.dispatcher_v2 import DispatcherV2

async def main():
    dispatcher = DispatcherV2()
    
    print("\n" + "="*80)
    print("🤖 AETHER OS CLI - 17 Agentes")
    print("="*80 + "\n")
    
    dispatcher.list_agents()
    
    while True:
        print("\n" + "-"*80)
        request = input("📝 Describe tu proyecto (o 'salir'): ").strip()
        
        if request.lower() == "salir":
            print("✅ Hasta luego!")
            break
        
        if not request:
            print("⚠️ Por favor describe algo")
            continue
        
        results = await dispatcher.execute(request)
        
        print("\n📊 RESULTADOS:")
        for agent, result in results.items():
            status = "✅" if result["status"] == "completed" else "❌"
            print(f"{status} {agent}")

if __name__ == "__main__":
    asyncio.run(main())
