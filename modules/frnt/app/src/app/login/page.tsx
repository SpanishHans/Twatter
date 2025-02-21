import Button from "@/components/Button";
import Footer from "@/components/Footer";
import Logo from "@/components/Logo";

export default function Home() {
  return (
    <div className="flex flex-col bg-caret-blue-950 min-h-screen">
      <main className="flex flex-col items-center justify-center bg-black min-h-full grow">
        
          <div className="flex flex-row min-h-full grow">

            <div className="hidden sm:flex min-w-[50vw] items-center justify-center bg-white min-h-full grow">
              <Logo />
            </div>
            
            <div className="flex md:min-w-[50vw] w-full">
              <div className="m-12 md:ml-20 grow flex flex-col justify-between">
                
                <div>
                  <h1 className="text-5xl font-bold break-all">Iniciar Sesión</h1>
                </div>
                
                <div className="flex flex-col w-full sm:w-[300px]">
                  <form className="flex flex-col w-full">
                    <input
                      type="text"
                      placeholder="Nombre de usuario"
                      className="mb-4 p-3 rounded-md bg-gray-800 text-white"
                    />
                    <input
                      type="password"
                      placeholder="Contraseña"
                      className="mb-4 p-3 rounded-md bg-gray-800 text-white"
                    />
  
                    <Button variant="blue" className="mb-4" href="/register">
                      Inciar Sesión
                    </Button>
                  </form>
  
                  <div className="flex items-center my-4">
                    <div className="flex-grow border-t border-gray-300"></div>
                    <span className="px-4 text-white">ó</span>
                    <div className="flex-grow border-t border-gray-300"></div>
                  </div>
                  
                  <div className="flex flex-row mb-4 gap-2">
                    <Button variant="white" className="w-1/2">Google</Button>
                    <Button variant="white" className="w-1/2">Apple</Button>
                  </div>
  
                  <div className="text-xs text-gray-500">
                    Al registrarse, acepta nuestros términos y condiciones.
                  </div>
                </div>
                
                <div className="flex flex-col w-full sm:w-[300px]">
                  <span className="mb-2 font-extrabold">¿Aún no te has registrado?</span>
                  <Button variant="outline" href="/register">Registrarse</Button>
                </div>
                
              </div>
            </div>
            
          </div>
          
          <Footer />
          
        
      </main>
    </div>
  );
}
