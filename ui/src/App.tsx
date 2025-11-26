import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet'; // Import Leaflet library
import 'leaflet/dist/leaflet.css'; // Import Leaflet CSS
import { Leaf, Camera, Egg, Shield, Sparkles, TrendingUp, ChevronRight, MessageCircle, Navigation } from 'lucide-react';
import { About } from './About';
import { Privacy } from './Privacy';

function App() {
  const [wasteCount, setWasteCount] = useState(1247);
  const [currentPage, setCurrentPage] = useState<'home' | 'about' | 'privacy'>('home');

  useEffect(() => {
    const interval = setInterval(() => {
      setWasteCount(prev => prev + Math.floor(Math.random() * 3));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  if (currentPage === 'about') {
    return <About onBack={() => setCurrentPage('home')} />;
  }

  if (currentPage === 'privacy') {
    return <Privacy onBack={() => setCurrentPage('home')} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-stone-50 to-amber-50">
      <Navbar onNavigate={setCurrentPage} />
      <HeroSection wasteCount={wasteCount} />
      <FeaturesGrid />
      <WasteMapPreview />
      <Footer />
    </div>
  );
}

function Navbar({ onNavigate }: { onNavigate: (page: 'home' | 'about' | 'privacy') => void }) {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-stone-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <button onClick={() => onNavigate('home')} className="flex items-center gap-2">
            <div className="relative">
              <Leaf className="w-8 h-8 text-emerald-600" strokeWidth={2.5} />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-amber-500 rounded-full animate-pulse" />
            </div>
            <span className="text-xl font-bold text-stone-800">EcoCycle ID</span>
          </button>

          <div className="hidden md:flex items-center gap-8">
            <button onClick={() => onNavigate('home')} className="text-stone-600 hover:text-emerald-600 transition-colors font-medium">Beranda</button>
            <a href="#mitra" className="text-stone-600 hover:text-emerald-600 transition-colors font-medium">Mitra</a>
            <a href="#peta" className="text-stone-600 hover:text-emerald-600 transition-colors font-medium">Peta Limbah</a>
            <button onClick={() => onNavigate('about')} className="text-stone-600 hover:text-emerald-600 transition-colors font-medium">Tentang Kami</button>
            <button onClick={() => onNavigate('privacy')} className="text-stone-600 hover:text-emerald-600 transition-colors font-medium">Kebijakan Privasi</button>
          </div>

          <button className="bg-gradient-to-r from-emerald-600 to-emerald-700 text-white px-6 py-2.5 rounded-full font-semibold hover:shadow-lg hover:scale-105 transition-all duration-200">
            Gabung Sekarang
          </button>
        </div>
      </div>
    </nav>
  );
}

function HeroSection({ wasteCount }: { wasteCount: number }) {
  return (
    <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12 space-y-6">
          <div className="inline-flex items-center gap-2 bg-emerald-100 text-emerald-700 px-4 py-2 rounded-full text-sm font-semibold mb-4">
            <Sparkles className="w-4 h-4" />
            <span>ITB Hackathon 2025 Innovation</span>
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-stone-800 leading-tight">
            Ubah Limbah Makanan<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-amber-600">
              Menjadi Cuan & Pakan
            </span>
          </h1>

          <p className="text-xl text-stone-600 max-w-3xl mx-auto leading-relaxed">
            Marketplace limbah organik pertama di Indonesia. Hubungkan dapur Anda dengan peternak lokal dalam satu klik.
          </p>

          <div className="flex items-center justify-center gap-2 text-stone-700 bg-white/60 backdrop-blur-sm px-6 py-3 rounded-full inline-flex border border-emerald-200">
            <TrendingUp className="w-5 h-5 text-emerald-600" />
            <span className="font-bold text-2xl text-emerald-600">{wasteCount.toLocaleString('id-ID')}</span>
            <span className="text-sm">Kg Limbah Terselamatkan Minggu Ini</span>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6 max-w-5xl mx-auto mt-16">
          <ActionCard
            icon={<Camera className="w-10 h-10" />}
            title="Saya Punya Sampah"
            subtitle="Untuk Resto/Warga"
            description="Jual limbah organik Anda, dapatkan poin & uang"
            gradient="from-emerald-500 to-emerald-600"
            hoverGradient="from-emerald-600 to-emerald-700"
          />

          <ActionCard
            icon={<Egg className="w-10 h-10" />}
            title="Cari Pakan/Kompos"
            subtitle="Untuk Peternak"
            description="Akses pakan maggot & kompos berkualitas murah"
            gradient="from-amber-500 to-orange-600"
            hoverGradient="from-amber-600 to-orange-700"
          />
        </div>
      </div>
    </section>
  );
}

function ActionCard({ icon, title, subtitle, description, gradient, hoverGradient }: {
  icon: React.ReactNode;
  title: string;
  subtitle: string;
  description: string;
  gradient: string;
  hoverGradient: string;
}) {
  return (
    <button className={`group relative overflow-hidden bg-gradient-to-br ${gradient} hover:${hoverGradient} p-8 rounded-3xl text-white text-left transition-all duration-300 hover:scale-105 hover:shadow-2xl`}>
      <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16 group-hover:scale-150 transition-transform duration-500" />

      <div className="relative z-10">
        <div className="bg-white/20 backdrop-blur-sm w-16 h-16 rounded-2xl flex items-center justify-center mb-4 group-hover:bg-white/30 transition-colors">
          {icon}
        </div>

        <h3 className="text-2xl font-bold mb-1">{title}</h3>
        <p className="text-white/80 text-sm font-medium mb-3">{subtitle}</p>
        <p className="text-white/90 text-base leading-relaxed">{description}</p>

        <div className="flex items-center gap-2 mt-6 text-sm font-semibold">
          <span>Mulai Sekarang</span>
          <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
        </div>
      </div>
    </button>
  );
}

function FeaturesGrid() {
  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-stone-800 mb-4">
            Kenapa Pilih EcoCycle ID?
          </h2>
          <p className="text-xl text-stone-600">
            Teknologi terdepan untuk solusi limbah berkelanjutan
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Sparkles className="w-8 h-8" />}
            title="AI Scan"
            description="Deteksi jenis sampah otomatis dengan AI. Cukup foto, sistem kami akan klasifikasi dan tentukan harga optimal."
            color="emerald"
          />

          <FeatureCard
            icon={<Shield className="w-8 h-8" />}
            title="Privacy First"
            description="Lokasi Anda disamarkan (Geohashing) untuk keamanan. Privasi adalah prioritas utama kami."
            color="blue"
          />

          <FeatureCard
            icon={<TrendingUp className="w-8 h-8" />}
            title="Cuan"
            description="Dapatkan poin atau uang dari sampah terpilah. Kontribusi kecil Anda bernilai ekonomi nyata."
            color="amber"
          />
        </div>
      </div>
    </section>
  );
}

function FeatureCard({ icon, title, description, color }: {
  icon: React.ReactNode;
  title: string;
  description: string;
  color: string;
}) {
  const colorMap: Record<string, { bg: string; icon: string; border: string }> = {
    emerald: { bg: 'bg-emerald-50', icon: 'text-emerald-600', border: 'border-emerald-200' },
    blue: { bg: 'bg-blue-50', icon: 'text-blue-600', border: 'border-blue-200' },
    amber: { bg: 'bg-amber-50', icon: 'text-amber-600', border: 'border-amber-200' }
  };

  const colors = colorMap[color];

  return (
    <div className={`${colors.bg} p-8 rounded-2xl border ${colors.border} hover:shadow-xl transition-all duration-300 hover:-translate-y-1`}>
      <div className={`${colors.icon} mb-4`}>
        {icon}
      </div>
      <h3 className="text-2xl font-bold text-stone-800 mb-3">{title}</h3>
      <p className="text-stone-600 leading-relaxed">{description}</p>
    </div>
  );
}

// Define interface for waste post data
interface WastePost {
  id: number;
  provider_type: string;
  waste_category: string;
  suitable_for: string;
  weight_est: number;
  lat: number;
  lon: number;
  created_at: string;
  // image_blob: string; // Not directly used on map
  // ai_analysis: string; // Not directly used on map
}

// Helper function for suitability emojis (replicated from main.py)
function getSuitabilityEmojis(tagsString: string): string {
  const emojis: string[] = [];
  if (tagsString.includes('Maggot')) emojis.push("🐛");
  if (tagsString.includes('Ayam') || tagsString.includes('Unggas')) emojis.push("🐔");
  if (tagsString.includes('Pupuk Kompos')) emojis.push("🌱");
  if (tagsString.includes('Ikan')) emojis.push("🐟");
  if (tagsString.includes('Biogas')) emojis.push("💨");
  return emojis.join(" ");
}

// Custom icon logic
const createCustomIcon = (color: string) => {
  let iconHtml = `
    <div style="
      background-color: ${color};
      width: 30px;
      height: 30px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 14px;
      font-weight: bold;
      border: 3px solid white;
      box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    ">
      ♻️
    </div>`;

  return L.divIcon({
    className: 'custom-div-icon',
    html: iconHtml,
    iconSize: [30, 30],
    iconAnchor: [15, 30], // Center the icon at the marker's location
    popupAnchor: [0, -25] // Adjust popup anchor
  });
};

const greenIcon = createCustomIcon('#10b981'); // Emerald
const orangeIcon = createCustomIcon('#f59e0b'); // Amber
const redIcon = createCustomIcon('#ef4444');   // Red

function getMarkerIcon(post: WastePost) {
  const suitableFor = post.suitable_for.toLowerCase();
  if (suitableFor.includes('sayur') || suitableFor.includes('kompos')) {
    return greenIcon;
  }
  if (suitableFor.includes('makanan') || suitableFor.includes('ayam') || suitableFor.includes('maggot')) {
    return orangeIcon;
  }
  return redIcon;
}

// Map component with dynamic centering
function MapUpdater({ posts }: { posts: WastePost[] }) {
  const map = useMap();

  useEffect(() => {
    if (posts.length > 0) {
      const latLngs = posts.map(post => [post.lat, post.lon]);
      // @ts-ignore
      const bounds = L.latLngBounds(latLngs);
      map.fitBounds(bounds, { padding: [50, 50] }); // Add some padding
    } else {
      map.setView([-6.2088, 106.8456], 11); // Default Jakarta
    }
  }, [posts, map]);

  return null;
}


// WasteMapPreview Component - this is the main one to replace
function WasteMapPreview() {
  const [wastePosts, setWastePosts] = useState<WastePost[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWastePosts = async () => {
      try {
        setLoading(true);
        // Assuming your FastAPI runs on port 8000
        const response = await fetch('http://localhost:8000/waste_posts');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: WastePost[] = await response.json();
        setWastePosts(data);
      } catch (err) {
        setError("Failed to fetch waste posts. Please ensure the backend API is running (e.g., uvicorn api:app --reload --port 8000).");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchWastePosts();
    // Refresh data every 30 seconds
    const interval = setInterval(fetchWastePosts, 30000);
    return () => clearInterval(interval);
  }, []);

  // Default center and zoom if no posts or still loading
  const defaultCenter: [number, number] = [-6.2088, 106.8456]; // Jakarta
  const defaultZoom = 11;

  if (loading) {
    return (
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-stone-50 to-emerald-50">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-lg text-stone-600">Loading map data...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-stone-50 to-emerald-50">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-lg text-red-600">{error}</p>
        </div>
      </section>
    );
  }


  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-stone-50 to-emerald-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl sm:text-5xl font-bold text-stone-800 mb-4">
            Peta Limbah Real-Time
          </h2>
          <p className="text-xl text-stone-600">
            Temukan limbah organik terdekat di sekitar Anda.
          </p>
        </div>

        <div className="relative bg-white rounded-3xl p-2 shadow-2xl overflow-hidden aspect-video"> {/* Removed p-8, added p-2, aspect-video for consistent sizing */}
          <MapContainer center={defaultCenter} zoom={defaultZoom} scrollWheelZoom={true} className="h-full w-full rounded-2xl z-0">
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {wastePosts.map(post => {
              const emojis = getSuitabilityEmojis(post.suitable_for);
              const phoneNumber = "6285388156854";
              const messageText = `Halo, saya tertarik dengan limbah *${post.waste_category}* (${post.weight_est}kg) dari ${post.provider_type}. Apakah masih tersedia?`;
              const encodedMessage = encodeURIComponent(messageText);
              const whatsappLink = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
              const googleMapsLink = `https://www.google.com/maps/dir/?api=1&destination=${post.lat},${post.lon}`;

              return (
                <Marker key={post.id} position={[post.lat, post.lon]} icon={getMarkerIcon(post)}>
                  <Popup>
                    <div className="font-sans text-sm p-1">
                      <div className="bg-emerald-100 text-emerald-800 px-2 py-1 rounded text-xs font-semibold mb-1 inline-block">
                        {post.provider_type}
                      </div>
                      <h4 className="font-bold text-stone-800 text-base mb-1">{post.waste_category}</h4>
                      <p className="text-stone-700 mb-1">
                        Berat: <span className="font-bold">{post.weight_est.toFixed(1)} kg</span>
                      </p>
                      <p className="text-stone-600 mb-2">
                        Cocok untuk: {post.suitable_for} {emojis}
                      </p>
                      <a
                        href={whatsappLink}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-emerald-500 hover:bg-emerald-600 text-white font-semibold py-2 px-3 rounded-md flex items-center justify-center gap-1 mb-2 transition-colors"
                      >
                        <MessageCircle size={16} /> Hubungi via WA
                      </a>
                      <a
                        href={googleMapsLink}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-500 hover:text-blue-700 text-xs flex items-center justify-center gap-1"
                      >
                        <Navigation size={14} /> Navigasi ke Lokasi
                      </a>
                    </div>
                  </Popup>
                </Marker>
              );
            })}
            <MapUpdater posts={wastePosts} />
          </MapContainer>
        </div>

        <div className="mt-8 text-center">
          <p className="text-stone-600 mb-4">
            Lokasi disamarkan untuk privasi. Kontak langsung setelah match.
          </p>
          <button className="bg-gradient-to-r from-emerald-600 to-emerald-700 text-white px-8 py-3 rounded-full font-semibold hover:shadow-lg hover:scale-105 transition-all duration-200 inline-flex items-center gap-2">
            <span>Lihat Peta Lengkap</span>
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="bg-stone-800 text-stone-300 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <Leaf className="w-8 h-8 text-emerald-500" strokeWidth={2.5} />
            <span className="text-xl font-bold text-white">EcoCycle ID</span>
          </div>

          <div className="text-center md:text-right">
            <p className="text-sm">
              © 2025 EcoCycle ID - ITB Hackathon Team
            </p>
            <p className="text-xs text-stone-400 mt-1">
              Membangun masa depan berkelanjutan, satu limbah pada satu waktu
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default App;
