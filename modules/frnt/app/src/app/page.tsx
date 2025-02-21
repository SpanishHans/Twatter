import Button from "@/components/Button";
import Footer from "@/components/Footer";
import Logo from "@/components/Logo";
import TrendingCarousel from "@/components/Popular";

import { FaGoogle } from "react-icons/fa";
import { AiFillApple } from "react-icons/ai";

export default function Home() {
  return (
    <div className="flex flex-col bg-caret-blue-950 min-h-screen">
      <main className="flex flex-col items-center justify-center min-h-full grow">
        
          <div className="flex flex-row min-h-full grow">
  
            <div className="hidden sm:flex min-w-[50vw] items-center justify-center bg-white min-h-full grow">
              <Logo width={300} height={300} />
            </div>
  
            <div className="flex md:min-w-[50vw] w-full">
              <div className="m-12 md:ml-20 grow flex flex-col justify-between">
                
                <div>
                  <TrendingCarousel />

                  <h1 className="text-4xl font-bold my-8">Únete ahora.</h1>
                </div>
                  
                <div className="flex flex-col w-full sm:w-[300px]">
                  <Button variant="white" icon={<FaGoogle className="w-5 h-5" />} className="mb-[10px]">Google</Button>
                  <Button variant="white" icon={<AiFillApple className="w-7 h-7" />} className="mb-[0px]">Apple</Button>

                  <div className="flex items-center my-4">
                    <div className="flex-grow border-t border-gray-300"></div>
                    <span className="px-4 text-white">ó</span>
                    <div className="flex-grow border-t border-gray-300"></div>
                  </div>

                  <Button
                    variant="blue"
                    className="mb-[8px]"
                    href="/register"
                  >
                    Crear una cuenta
                  </Button>

                  <div className="text-xs text-gray-500 mb-[20px]">
                    Al crear una cuenta usted accede a nuestra venta de datos a terceros.
                  </div>
                </div>
                
                <div className="flex flex-col w-full sm:w-[300px]">
                  <span className="mb-2 font-extrabold">¿Ya tienes una cuenta?</span>
                  <Button variant="outline" href="/login">Inicia sesión</Button>
                </div>
                
              </div>
            </div>
            
          </div>
          
          <Footer />
          
        
      </main>
    </div>
  );
}
