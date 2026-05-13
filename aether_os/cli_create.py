"""AETHER OS - CLI que crea lo que pidas."""

import asyncio
from aether_os.execution_engine_real import RealExecutionEngineV2


async def main():
    engine = RealExecutionEngineV2()
    
    print("\n" + "="*70)
    print("AETHER OS - Generador de Apps")
    print("="*70 + "\n")
    
    while True:
        print("OPCIONES:")
        print("1. Crear app personalizada")
        print("2. Crear TODO app")
        print("3. Crear Dashboard")
        print("4. Crear API REST")
        print("5. Salir\n")
        
        choice = input("Elige (1-5): ").strip()
        
        if choice == "1":
            spec = input("\nDescribe tu app: ").strip()
            name = input("Nombre del proyecto: ").strip()
            if spec and name:
                result = await engine.create_complete_app(spec, name)
                print(f"\nApp creada en: {result['path']}\n")
        
        elif choice == "2":
            result = await engine.create_complete_app(
                "TODO app with add/delete/complete functionality",
                "todo_app"
            )
            print(f"\nApp creada en: {result['path']}\n")
        
        elif choice == "3":
            result = await engine.create_complete_app(
                "Analytics dashboard with charts and real-time data",
                "dashboard_app"
            )
            print(f"\nApp creada en: {result['path']}\n")
        
        elif choice == "4":
            result = await engine.create_complete_app(
                "REST API with authentication, users, and products endpoints",
                "api_rest"
            )
            print(f"\nApp creada en: {result['path']}\n")
        
        elif choice == "5":
            print("\nHasta luego!\n")
            break
        
        else:
            print("Opcion invalida\n")


if __name__ == "__main__":
    asyncio.run(main())
