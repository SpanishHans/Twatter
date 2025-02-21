import Button from "@/components/Button";
import Logo from "@/components/Logo";

export default function Dashboard() {
  return (
    <div className="flex min-h-screen bg-black text-white">
      {/* Left Sidebar */}
      <aside className="w-64 p-4 flex flex-col gap-6 border-r border-gray-800">
        <Logo />
        <nav className="flex flex-col gap-4">
          <Button variant="white" href="/">Home</Button>
          <Button variant="outline" href="/explore">Explore</Button>
          <Button variant="outline" href="/notifications">Notifications</Button>
          <Button variant="outline" href="/messages">Messages</Button>
        </nav>
        <Button variant="blue" href="/tweet">Tweet</Button>
      </aside>

      {/* Center Feed */}
      <main className="flex-1 p-8 overflow-y-auto">
        <div className="mb-6">
          <input
            type="text"
            placeholder="Search Twatter"
            className="w-full p-2 rounded-full bg-gray-900 text-white placeholder-gray-500 focus:outline-none"
          />
        </div>

        <h1 className="text-2xl font-bold mb-6">Home</h1>

        <div className="space-y-6">
          {[1, 2, 3, 4, 5].map((tweet) => (
            <div key={tweet} className="border-b border-gray-700 pb-4">
              <h2 className="font-semibold">User {tweet}</h2>
              <p>This is a sample tweet number {tweet}. Welcome to Twatter!</p>
            </div>
          ))}
        </div>
      </main>

      {/* Right Sidebar */}
      <aside className="w-64 p-4 flex flex-col gap-6 border-l border-gray-800">
        <h2 className="text-xl font-bold mb-4">Novedades</h2>
        <div className="space-y-4">
          {["#TwatterLaunch", "#DramaMinisterial", "#OpenSource"].map((trend, index) => (
            <div key={index} className="text-sm">
              <p className="font-semibold">{trend}</p>
              <p className="text-gray-500">Trending now</p>
            </div>
          ))}
        </div>
      </aside>
    </div>
  );
}
