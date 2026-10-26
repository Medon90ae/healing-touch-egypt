import React from 'react';
import { ShoppingBag, ShieldCheck } from 'lucide-react';

interface MobileStickyBarProps {
  onOpenCheckout: () => void;
  cartCount: number;
}

export const MobileStickyBar: React.FC<MobileStickyBarProps> = ({
  onOpenCheckout,
  cartCount
}) => {
  return (
    <div className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md border-t border-[#e2ece6] px-4 py-3 shadow-[0_-4px_20px_rgba(6,78,59,0.08)]">
      <div className="max-w-md mx-auto flex items-center justify-between gap-3 text-right">
        
        {/* Price & Guarantee */}
        <div className="shrink-0">
          <div className="flex items-center gap-1.5 text-[11px] font-semibold text-[#059669]">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>معتمد سريرياً للقيصرية</span>
          </div>
          <div className="flex items-baseline gap-1 mt-0.5">
            <span className="text-lg font-extrabold text-[#064e3b] tabular-nums">
              890 ج.م
            </span>
            <span className="text-xs text-[#707974] line-through tabular-nums">
              1,290 ج.م
            </span>
            <span className="text-[10px] text-[#059669] font-bold mr-1">
              (شحن مجاني)
            </span>
          </div>
        </div>

        {/* CTA Button */}
        <button
          onClick={onOpenCheckout}
          className="flex-1 py-3 px-4 rounded-xl text-xs sm:text-sm font-bold text-white bg-[#064e3b] hover:bg-[#003527] transition-all shadow-sm active:scale-[0.98] flex items-center justify-center gap-2 cursor-pointer"
        >
          <ShoppingBag className="w-4 h-4 text-[#82f5c1]" />
          <span>{cartCount > 0 ? `إتمام الطلب (${cartCount})` : 'طلب باقة التعافي'}</span>
        </button>

      </div>
    </div>
  );
};
