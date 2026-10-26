import React from 'react';
import { ShoppingBag, ShieldCheck, ClipboardCheck } from 'lucide-react';

interface HeaderProps {
  cartCount: number;
  onOpenCart: () => void;
  onOpenOrders: () => void;
  onScrollTo: (sectionId: string) => void;
}

export const Header: React.FC<HeaderProps> = ({
  cartCount,
  onOpenCart,
  onOpenOrders,
  onScrollTo
}) => {
  return (
    <header className="sticky top-0 z-40 bg-[#fbfdfb]/95 backdrop-blur-md border-b border-[#e2ece6]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between gap-8">
        {/* Zone 1: Brand Wordmark (Single Text Element) */}
        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            className="flex items-center gap-2.5 text-right group"
          >
            <div className="w-10 h-10 rounded-xl bg-[#064e3b] text-[#fbfdfb] flex items-center justify-center shadow-sm group-hover:bg-[#059669] transition-colors">
              <ShieldCheck className="w-5 h-5 text-[#82f5c1]" />
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-bold tracking-tight text-[#064e3b] whitespace-nowrap">
                هيلينج تاتش مصر
              </span>
              <span className="text-[11px] font-medium text-[#059669] whitespace-nowrap">
                بروتوكول التعافي وحماية القيصرية
              </span>
            </div>
          </button>
        </div>

        {/* Zone 2: Navigation Links (Single-Line, Whitespace-Nowrap) */}
        <nav className="hidden lg:flex items-center gap-7 text-sm font-medium text-[#404944]">
          <button
            onClick={() => onScrollTo('calculator')}
            className="hover:text-[#064e3b] transition-colors whitespace-nowrap py-1 cursor-pointer"
          >
            حاسبة الشاور والجاهزية
          </button>
          <button
            onClick={() => onScrollTo('stages')}
            className="hover:text-[#064e3b] transition-colors whitespace-nowrap py-1 cursor-pointer"
          >
            مراحل التئام القيصرية
          </button>
          <button
            onClick={() => onScrollTo('products')}
            className="hover:text-[#064e3b] transition-colors whitespace-nowrap py-1 cursor-pointer"
          >
            باقات البروتوكول
          </button>
          <button
            onClick={() => onScrollTo('comparison')}
            className="hover:text-[#064e3b] transition-colors whitespace-nowrap py-1 cursor-pointer"
          >
            المقارنة السريرية
          </button>
          <button
            onClick={() => onScrollTo('faq')}
            className="hover:text-[#064e3b] transition-colors whitespace-nowrap py-1 cursor-pointer"
          >
            الأسئلة الشائعة
          </button>
          <button
            onClick={onOpenOrders}
            className="flex items-center gap-1.5 text-[#059669] hover:text-[#064e3b] font-semibold transition-colors whitespace-nowrap py-1 cursor-pointer"
          >
            <ClipboardCheck className="w-4 h-4" />
            <span>متابعة طلباتي</span>
          </button>
        </nav>

        {/* Zone 3: Primary Action & Cart Trigger */}
        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={onOpenCart}
            aria-label="سلة المشتريات"
            className="relative p-2.5 rounded-lg border border-[#e2ece6] bg-white text-[#064e3b] hover:bg-[#f3f7f5] transition-colors cursor-pointer flex items-center justify-center"
          >
            <ShoppingBag className="w-5 h-5 text-[#064e3b]" />
            {cartCount > 0 && (
              <span className="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full bg-[#059669] text-white text-[11px] font-bold flex items-center justify-center shadow-sm">
                {cartCount}
              </span>
            )}
          </button>

          <button
            onClick={() => onScrollTo('products')}
            className="hidden sm:inline-flex items-center justify-center px-4.5 py-2.5 rounded-lg text-xs md:text-sm font-semibold text-white bg-[#064e3b] hover:bg-[#003527] transition-all shadow-sm active:scale-[0.98] whitespace-nowrap cursor-pointer"
          >
            طلب البروتوكول الطبي
          </button>
        </div>
      </div>
    </header>
  );
};
