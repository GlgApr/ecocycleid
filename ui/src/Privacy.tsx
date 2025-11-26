import { Shield, Lock, ArrowLeft } from 'lucide-react';

interface PrivacyProps {
  onBack: () => void;
}

export function Privacy({ onBack }: PrivacyProps) {
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

        <section className="bg-white rounded-2xl p-8 shadow-lg border border-stone-200">
          <div className="mb-8 border-b border-stone-100 pb-4">
             <h2 className="text-3xl font-bold text-stone-800 mb-4 flex items-center gap-3">
              <Shield className="w-8 h-8 text-emerald-600" />
              Kebijakan Privasi
            </h2>
            <p className="text-sm text-stone-500">
              Terakhir diperbarui: 26 November 2025
            </p>
          </div>

          <div className="space-y-6 text-stone-700">
            <p>
              Di EcoCycle ID, kami menghargai privasi Anda dan berkomitmen untuk melindungi data pribadi Anda sesuai dengan <strong>Undang-Undang Pelindungan Data Pribadi (UU PDP)</strong> di Indonesia dan standar global seperti <strong>GDPR</strong>.
            </p>

            <PrivacyPoint 
              title="1. Pengumpulan Data"
              content="Kami mengumpulkan data yang diperlukan untuk layanan kami, termasuk nama, lokasi (yang disamarkan/geohashed), dan data transaksi limbah. Kami hanya mengumpulkan data yang Anda berikan secara sukarela saat mendaftar atau menggunakan layanan."
            />

            <PrivacyPoint 
              title="2. Penggunaan Data"
              content="Data Anda digunakan untuk menghubungkan Anda dengan mitra daur ulang, memproses transaksi, dan meningkatkan layanan kami. Kami menggunakan AI untuk analisis jenis sampah tanpa mengidentifikasi wajah atau informasi sensitif lainnya dari foto."
            />

            <PrivacyPoint 
              title="3. Keamanan Data"
              content="Kami menerapkan langkah-langkah keamanan teknis dan organisasi yang sesuai untuk melindungi data Anda dari akses tidak sah, pencurian, atau perubahan, termasuk enkripsi data standar industri."
            />

            <PrivacyPoint 
              title="4. Hak Anda (UU PDP & GDPR)"
              content="Anda memiliki hak untuk mengakses, mengoreksi, menghapus, atau membatasi pemrosesan data pribadi Anda. Anda juga berhak untuk menarik persetujuan penggunaan data kapan saja dengan menghubungi kami."
            />

             <div className="bg-emerald-50 p-4 rounded-lg border border-emerald-100 mt-6">
              <h4 className="font-semibold text-emerald-800 mb-2 flex items-center gap-2">
                <Lock className="w-4 h-4" />
                Komitmen Kami
              </h4>
              <p className="text-sm text-emerald-700">
                Kami tidak akan pernah menjual data pribadi Anda kepada pihak ketiga tanpa persetujuan eksplisit dari Anda.
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

function PrivacyPoint({ title, content }: { title: string; content: string }) {
  return (
    <div>
      <h3 className="text-lg font-semibold text-stone-800 mb-2">{title}</h3>
      <p className="leading-relaxed text-stone-600">{content}</p>
    </div>
  );
}
