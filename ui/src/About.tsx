import { Users, ArrowLeft } from 'lucide-react';

interface AboutProps {
  onBack: () => void;
}

export function About({ onBack }: AboutProps) {
  return (
    <div className="min-h-screen bg-stone-50 pt-20 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <button 
          onClick={onBack}
          className="flex items-center gap-2 text-emerald-600 font-semibold mb-8 hover:text-emerald-700 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Kembali ke Beranda
        </button>

        <section className="mb-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-stone-800 mb-4 flex items-center justify-center gap-3">
              <Users className="w-8 h-8 text-emerald-600" />
              Tentang Kami
            </h2>
            <p className="text-stone-600">
              Tim di balik inovasi EcoCycle ID - Kombinasi 2 Hacker, 1 Hustler, dan 1 Hipster.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* 2 Hackers */}
            <TeamMember 
              role="Hacker" 
              name="Alex Kode" 
              desc="Tech Lead & AI Specialist. Mengubah kopi menjadi kode cerdas."
              emoji="💻"
            />
             <TeamMember 
              role="Hacker" 
              name="Sarah Algo" 
              desc="Backend & Security. Menjaga privasi dan data tetap aman."
              emoji="🔐"
            />
            {/* 1 Hustler */}
            <TeamMember 
              role="Hustler" 
              name="Budi Bisnis" 
              desc="CEO & Visionary. Menghubungkan titik-titik peluang pasar."
              emoji="🚀"
            />
            {/* 1 Hipster */}
            <TeamMember 
              role="Hipster" 
              name="Lisa Desain" 
              desc="UI/UX & Creative. Membuat pengalaman pengguna yang intuitif."
              emoji="🎨"
            />
          </div>
        </section>
      </div>
    </div>
  );
}

function TeamMember({ role, name, desc, emoji }: { role: string; name: string; desc: string; emoji: string }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-stone-200 text-center hover:shadow-md transition-all hover:-translate-y-1">
      <div className="text-4xl mb-4">{emoji}</div>
      <div className="inline-block px-3 py-1 bg-stone-100 text-stone-600 text-xs font-bold rounded-full mb-2 uppercase tracking-wider">
        {role}
      </div>
      <h3 className="text-lg font-bold text-stone-800 mb-2">{name}</h3>
      <p className="text-sm text-stone-500">{desc}</p>
    </div>
  );
}
