import React from 'react';
import { ShieldCheck, MessageCircle, PhoneCall, Award } from 'lucide-react';

interface FooterProps {
  onScrollTo: (sectionId: string) => void;
  onOpenOrders: () => void;
}

export const Footer: React.FC<FooterProps> = ({ onScrollTo, onOpenOrders }) => {
  return (
    <footer className="bg-[#f3f7f5] border-t border-[#e2ece6] text-right text-xs text-[#526058] pt-12 pb-24 lg:pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Top Footer Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          
          {/* Brand & Credential */}
          <div className="md:col-span-2 space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-[#064e3b] text-white flex items-center justify-center">
                <ShieldCheck className="w-4 h-4 text-[#82f5c1]" />
              </div>
              <span className="text-base font-bold text-[#064e3b]">
                هيلينج تاتش مصر — Healing Touch Egypt
              </span>
            </div>
            <p className="text-xs text-[#404944] leading-relaxed max-w-md">
              المنصة الطبية المتخصصة في بروتوكولات التعافي المتقدمة بعد الجراحة القيصرية. نقدم حلولاً جراحية معقمة لعزل ماء الشاور 100% وتسطيح الندبات بالسيليكون الطبي المعتمد لراحة الأمهات في مصر.
            </p>
            <div className="flex items-center gap-2 text-[11px] text-[#059669]">
              <Award className="w-4 h-4" />
              <span>مختبر ومطابق لمعايير الأجهزة الطبية الجراحية الاستهلاكية</span>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-2.5">
            <h4 className="text-xs font-bold text-[#064e3b]">أقسام البروتوكول</h4>
            <ul className="space-y-1.5 text-xs text-[#404944]">
              <li>
                <button
                  onClick={() => onScrollTo('calculator')}
                  className="hover:text-[#064e3b] transition-colors cursor-pointer"
                >
                  حاسبة الشاور والجاهزية
                </button>
              </li>
              <li>
                <button
                  onClick={() => onScrollTo('products')}
                  className="hover:text-[#064e3b] transition-colors cursor-pointer"
                >
                  باقات التعافي الثلاثية
                </button>
              </li>
              <li>
                <button
                  onClick={() => onScrollTo('comparison')}
                  className="hover:text-[#064e3b] transition-colors cursor-pointer"
                >
                  المقارنة السريرية مع الشاش
                </button>
              </li>
              <li>
                <button
                  onClick={() => onScrollTo('guide')}
                  className="hover:text-[#064e3b] transition-colors cursor-pointer"
                >
                  خطوات الاستحمام الآمن
                </button>
              </li>
              <li>
                <button
                  onClick={onOpenOrders}
                  className="hover:text-[#064e3b] font-semibold text-[#059669] transition-colors cursor-pointer"
                >
                  متابعة طلباتي وشحناتي
                </button>
              </li>
            </ul>
          </div>

          {/* Contact & Support */}
          <div className="space-y-2.5">
            <h4 className="text-xs font-bold text-[#064e3b]">الدعم والاستفسارات الطبية</h4>
            <p className="text-xs text-[#404944]">
              فريق صيدلاني وتمريضي متخصص للإجابة على استفسارات الأمهات حول القيصرية:
            </p>
            <div className="space-y-2 pt-1">
              <a
                href="https://wa.me/201000000000"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-white border border-[#e2ece6] text-xs font-bold text-[#059669] hover:bg-[#82f5c1]/10 transition-colors"
              >
                <MessageCircle className="w-4 h-4" />
                <span>محادثة واتساب طبية فورية</span>
              </a>
              <div className="flex items-center gap-2 text-[11px] text-[#526058]">
                <PhoneCall className="w-3.5 h-3.5 text-[#064e3b]" />
                <span>خدمة العملاء: يومياً من 9 ص حتى 10 م</span>
              </div>
            </div>
          </div>

        </div>

        {/* Medical Advisory Notice */}
        <div className="p-4 rounded-xl bg-white border border-[#e2ece6] text-[11px] text-[#526058] leading-relaxed">
          <strong className="text-[#064e3b] font-bold block mb-1">إخلاء مسؤولية سريري:</strong>
          المعلومات والأدوات التفاعلية الواردة في هذه المنصة مصممة للتوجيه والدعم التثقيفي والوقائي بعد الجراحة القيصرية. لا تغني هذه الإرشادات عن الاستشارة الطبية المباشرة مع طبيب النساء والتوليد المعالج أو مراجعته فوراً في حال ظهور حمى أو إفرازات مستمرة أو ألم غير محتمل.
        </div>

        {/* Bottom copyright */}
        <div className="pt-4 border-t border-[#e2ece6] flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-[#707974]">
          <p>© {new Date().getFullYear()} هيلينج تاتش مصر. جميع الحقوق محفوظة لبروتوكول الرعاية القيصرية.</p>
          <p className="flex items-center gap-3">
            <span>جمهورية مصر العربية</span>
            <span>·</span>
            <span>القاهرة - الجيزة - الإسكندرية وكافة المحافظات</span>
          </p>
        </div>

      </div>
    </footer>
  );
};
