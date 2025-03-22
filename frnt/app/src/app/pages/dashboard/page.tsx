import Logo from "@/components/Logo";
import TrendingCarousel from "@/components/Popular";
import Button from "@/components/Button";
import LButton from "@/components/LeftButton";

import { FaHome, FaCompass, FaBell, FaUser, FaEllipsisH } from "react-icons/fa";

export default function Feed() {
  return (
    <div className="flex flex-col bg-caret-blue-300 min-h-screen">
      <main className="flex flex-row justify-center min-h-full grow">
        
        {/* Left Sidebar */}
        <aside className="hidden md:flex flex-col w-[20vw] p-6 text-white border-r border-gray-700">
          <div className="mb-6">
            <Logo width={50} height={50} />
          </div>
          <nav className="mt-4 space-y-4">
            <LButton variant="noborder" icon={<FaHome className="w-7 h-7" />}>Inicio</LButton>
            <LButton variant="noborder" icon={<FaCompass className="w-7 h-7" />}>Explorar</LButton>
            <LButton variant="noborder" icon={<FaBell className="w-7 h-7" />}>Notificaciones</LButton>
            <LButton variant="noborder" icon={<FaUser className="w-7 h-7" />}>Perfil</LButton>
            <LButton variant="noborder" icon={<FaEllipsisH className="w-7 h-7" />}>Más</LButton>
          </nav>
          <Button variant="blue" className="mt-12">Twatt</Button>
        </aside>
        
        {/* Main Feed */}
        <section className="flex flex-col w-full md:w-[50vw] p-6 text-white border-r border-gray-700">
          <h1 className="text-2xl font-bold mb-4">Inicio</h1>
          <div className="p-4 bg-gray-800 rounded-lg mb-4">
            <textarea
              className="w-full bg-transparent text-white p-2 border border-gray-600 rounded-lg"
              placeholder="¿Qué está pasando?"
            />
            <Button variant="blue" className="mt-2 w-full">Twatt</Button>
          </div>
          <div className="space-y-4">
            {[...Array(5)].map((_, index) => (
              <div key={index} className="p-4 bg-gray-800 rounded-lg">
                <span className="font-bold">Usuario {index + 1}</span>
                <p className="mt-2 text-gray-300">Este es un twatt de prueba #{index + 1}</p>
              </div>
            ))}
          </div>
        </section>
        
        {/* Right Sidebar */}
        <aside className="hidden lg:flex flex-col w-[25vw] p-6 text-white">
          <h2 className="text-xl font-bold mb-4">Tendencias</h2>
          <TrendingCarousel />
        </aside>
        
      </main>
    </div>
  );
}
