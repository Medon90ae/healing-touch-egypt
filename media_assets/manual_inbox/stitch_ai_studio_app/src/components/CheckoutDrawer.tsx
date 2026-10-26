import React, { useState } from 'react';
import { CartItem, Order, PaymentMethod } from '../types/protocol';
import { EGYPTIAN_GOVERNORATES } from '../data/protocolData';
import {
  X,
  Plus,
  Minus,
  Trash2,
  ShieldCheck,
  Truck,
  CheckCircle2,
  AlertCircle,
  Copy,
  Check,
  Send,
  Printer
} from 'lucide-react';

interface CheckoutDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  cart: CartItem[];
  onUpdateQuantity: (productId: string, quantity: number) => void;
  onRemoveItem: (productId: string) => void;
  onClearCart: () => void;
  onOrderPlaced: (order: Order) => void;
}

export const CheckoutDrawer: React.FC<CheckoutDrawerProps> = ({
  isOpen,
  onClose,
  cart,
  onUpdateQuantity,
  onRemoveItem,
  onClearCart,
  onOrderPlaced
}) => {
  const [customerName, setCustomerName] = useState('');
  const [phone, setPhone] = useState('');
  const [selectedGovId, setSelectedGovId] = useState('cairo');
  const [address, setAddress] = useState('');
  const [notes, setNotes] = useState('');
  const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>('cod');
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [confirmedOrder, setConfirmedOrder] = useState<Order | null>(null);
  const [copiedInstapay, setCopiedInstapay] = useState(false);

  if (!isOpen) return null;

  const selectedGov =
    EGYPTIAN_GOVERNORATES.find((g) => g.id === selectedGovId) || EGYPTIAN_GOVERNORATES[0];

  // Pricing calculations
  const subtotal = cart.reduce(
    (sum, item) => sum + item.product.priceEGP * item.quantity,
    0
  );

  // Free shipping if contains complete bundle or subtotal >= 800 EGP
  const hasBundle = cart.some((item) => item.product.id === 'complete-protocol-bundle');
  const isFreeShipping = hasBundle || subtotal >= 800;
  const shippingFee = isFreeShipping ? 0 : selectedGov.shippingFeeEGP;
  const total = subtotal + shippingFee;

  const validatePhone = (val: string) => {
    // Egyptian phone: 11 digits starting with 010, 011, 012, or 015
    const clean = val.replace(/\s+/g, '');
    const regex = /^01[0125][0-9]{8}$/;
    return regex.test(clean);
  };

  const handleCheckout = (e: React.FormEvent) => {
    e.preventDefault();
    const errors: Record<string, string> = {};

    if (!customerName.trim() || customerName.trim().length < 3) {
      errors.name = 'يرجى كتابة الاسم الثلاثي أو الثنائي بالكامل';
    }

    if (!validatePhone(phone)) {
      errors.phone = 'يرجى إدخال رقم موبايل مصري صحيح مكون من 11 رقماً (مثال: 01012345678)';
    }

    if (!address.trim() || address.trim().length < 8) {
      errors.address = 'يرجى كتابة العنوان بالتفصيل (اسم الشارع، رقم العمارة، والشقة أو علامة مميزة)';
    }

    if (cart.length === 0) {
      errors.cart = 'سلة المشتريات فارغة، يرجى إضافة المنتجات أولاً';
    }

    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    setFormErrors({});

    // Generate Order
    const randomNum = Math.floor(1000 + Math.random() * 9000);
    const orderNumber = `HT-EG-${randomNum}`;

    const newOrder: Order = {
      id: crypto.randomUUID(),
      orderNumber,
      customerName: customerName.trim(),
      phone: phone.trim(),
      governorate: selectedGov.nameAr,
      address: address.trim(),
      notes: notes.trim() || undefined,
      paymentMethod,
      items: cart.map((item) => ({
        productId: item.product.id,
        titleAr: item.product.titleAr,
        quantity: item.quantity,
        priceEGP: item.product.priceEGP
      })),
      subtotalEGP: subtotal,
      shippingFeeEGP: shippingFee,
      discountEGP: hasBundle ? 400 : 0,
      totalEGP: total,
      createdAt: new Date().toISOString(),
      status: 'confirmed',
      estimatedDeliveryAr: selectedGov.deliveryDaysAr
    };

    // Save locally and pass to parent
    const existingOrdersJson = localStorage.getItem('healing_touch_orders');
    const existingOrders: Order[] = existingOrdersJson ? JSON.parse(existingOrdersJson) : [];
    localStorage.setItem(
      'healing_touch_orders',
      JSON.stringify([newOrder, ...existingOrders])
    );

    setConfirmedOrder(newOrder);
    onOrderPlaced(newOrder);
    onClearCart();
  };

  const copyInstaPayAccount = () => {
    navigator.clipboard.writeText('healingtouch@instapay');
    setCopiedInstapay(true);
    setTimeout(() => setCopiedInstapay(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-[#121c2a]/50 backdrop-blur-xs flex justify-end">
      <div className="w-full max-w-lg bg-white h-full shadow-2xl flex flex-col text-right animate-in slide-in-from-left duration-300">
        
        {/* Drawer Header */}
        <div className="px-5 py-4 border-b border-[#e2ece6] flex items-center justify-between bg-[#fbfdfb]">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-[#064e3b] text-white flex items-center justify-center">
              <ShieldCheck className="w-4 h-4 text-[#82f5c1]" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-[#064e3b]">
                {confirmedOrder ? 'تأكيد طلب التعافي القيصري' : 'سلة الطلب وإنهاء الشراء السريع'}
              </h3>
              <p className="text-[11px] text-[#526058]">
                {confirmedOrder
                  ? `رقم الطلب: ${confirmedOrder.orderNumber}`
                  : 'توصيل معقم وسريع لكافة محافظات مصر'}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            aria-label="إغلاق"
            className="p-1.5 rounded-lg text-[#707974] hover:bg-[#f3f7f5] hover:text-[#121c2a] transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Drawer Body */}
        <div className="flex-1 overflow-y-auto p-5 space-y-6">
          {confirmedOrder ? (
            /* Order Success View */
            <div className="space-y-6 text-right py-2">
              <div className="p-6 rounded-2xl bg-[#f3f7f5] border border-[#82f5c1] text-center space-y-3">
                <div className="w-14 h-14 rounded-full bg-[#059669] text-white mx-auto flex items-center justify-center shadow-md">
                  <CheckCircle2 className="w-8 h-8" />
                </div>
                <h4 className="text-lg font-bold text-[#064e3b]">
                  تم تسجيل طلبك بنجاح وجارٍ تجهيزه للتعقيم والشحن!
                </h4>
                <div className="inline-block px-3.5 py-1.5 rounded-lg bg-white border border-[#e2ece6] text-xs font-mono font-bold text-[#064e3b]">
                  كود التتبع: {confirmedOrder.orderNumber}
                </div>
                <p className="text-xs text-[#404944] leading-relaxed">
                  شكراً لثقتك في هيلينج تاتش مصر. سيصلك اتصال أو رسالة تأكيد عبر واتساب من فريق الرعاية قبل تحرك مندوب التوصيل لمنزلك.
                </p>
              </div>

              {/* Delivery ETA & Details */}
              <div className="p-4 rounded-xl bg-white border border-[#e2ece6] space-y-2.5 text-xs">
                <div className="flex justify-between text-[#526058]">
                  <span>العميلة الكريمة:</span>
                  <span className="font-bold text-[#121c2a]">{confirmedOrder.customerName}</span>
                </div>
                <div className="flex justify-between text-[#526058]">
                  <span>رقم الموبايل:</span>
                  <span className="font-bold text-[#121c2a] font-mono">{confirmedOrder.phone}</span>
                </div>
                <div className="flex justify-between text-[#526058]">
                  <span>المحافظة والعنوان:</span>
                  <span className="font-bold text-[#121c2a] text-left max-w-[240px]">
                    {confirmedOrder.governorate} - {confirmedOrder.address}
                  </span>
                </div>
                <div className="flex justify-between text-[#526058]">
                  <span>موعد التسليم المتوقع:</span>
                  <span className="font-bold text-[#059669]">{confirmedOrder.estimatedDeliveryAr}</span>
                </div>
                <div className="flex justify-between text-[#526058]">
                  <span>طريقة الدفع:</span>
                  <span className="font-bold text-[#064e3b]">
                    {confirmedOrder.paymentMethod === 'cod'
                      ? 'الدفع نقداً عند الاستلام (معاينة الشحنة أولاً)'
                      : 'تحويل فوري عبر إنستاباي (InstaPay)'}
                  </span>
                </div>
                <div className="flex justify-between text-[#526058] pt-2 border-t border-[#e2ece6]">
                  <span className="font-bold text-sm text-[#064e3b]">المبلغ الإجمالي المستحق:</span>
                  <span className="font-bold text-base text-[#059669] tabular-nums">
                    {confirmedOrder.totalEGP} ج.م
                  </span>
                </div>
              </div>

              {/* InstaPay Transfer Instructions if chosen */}
              {confirmedOrder.paymentMethod === 'instapay' && (
                <div className="p-4 rounded-xl bg-[#eff4ff] border border-[#dee9fc] space-y-3 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-[#064e3b]">بيانات التحويل الفوري عبر تطبيق InstaPay:</span>
                    <button
                      onClick={copyInstaPayAccount}
                      className="flex items-center gap-1 text-[11px] text-[#059669] font-bold hover:underline cursor-pointer"
                    >
                      {copiedInstapay ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                      <span>{copiedInstapay ? 'تم النسخ' : 'نسخ المعرف'}</span>
                    </button>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white border border-[#d9e3f6] font-mono font-bold text-sm text-[#064e3b] text-center">
                    healingtouch@instapay
                  </div>
                  <p className="text-[11px] text-[#404944] leading-relaxed">
                    افتحي تطبيق إنستاباي وحولي مبلغ <strong>{confirmedOrder.totalEGP} ج.م</strong> إلى المعرف أعلاه، واكتبي في خانة الملاحظات كود الطلب: <strong>{confirmedOrder.orderNumber}</strong>.
                  </p>
                </div>
              )}

              {/* Action Buttons */}
              <div className="space-y-2 pt-2">
                <a
                  href={`https://wa.me/201000000000?text=${encodeURIComponent(
                    `مرحباً هيلينج تاتش، لقد أتممت طلبي برقم: ${confirmedOrder.orderNumber} بمبلغ ${confirmedOrder.totalEGP} ج.م وأود المتابعة معكم.`
                  )}`}
                  target="_blank"
                  rel="noreferrer"
                  className="w-full py-3 px-4 rounded-xl text-xs sm:text-sm font-bold text-white bg-[#059669] hover:bg-[#006c4a] transition-all flex items-center justify-center gap-2 cursor-pointer shadow-sm"
                >
                  <Send className="w-4 h-4" />
                  <span>تأكيد الطلب الفوري عبر واتساب الطبي</span>
                </a>

                <button
                  onClick={() => window.print()}
                  className="w-full py-2.5 px-4 rounded-xl text-xs font-semibold text-[#064e3b] bg-[#f3f7f5] hover:bg-[#e2ece6] border border-[#e2ece6] transition-all flex items-center justify-center gap-2 cursor-pointer"
                >
                  <Printer className="w-4 h-4" />
                  <span>طباعة أو حفظ إيصال الطلب</span>
                </button>
              </div>
            </div>
          ) : (
            /* Cart Items & Form */
            <>
              {/* Cart Items List */}
              <div className="space-y-3">
                <div className="flex items-center justify-between text-xs font-bold text-[#064e3b]">
                  <span>محتويات الطلب:</span>
                  <span className="text-[#526058]">{cart.length} منتجات</span>
                </div>

                {cart.length === 0 ? (
                  <div className="py-8 text-center text-xs text-[#526058] bg-[#f3f7f5] rounded-xl border border-[#e2ece6]">
                    سلة المشتريات فارغة حالياً. اختاري منتجاً من باقات البروتوكول للبدء.
                  </div>
                ) : (
                  <div className="space-y-2.5">
                    {cart.map((item) => (
                      <div
                        key={item.product.id}
                        className="p-3 rounded-xl border border-[#e2ece6] bg-[#fbfdfb] flex items-center justify-between gap-3 text-xs"
                      >
                        <div className="flex-1">
                          <h4 className="font-bold text-[#064e3b] text-xs leading-snug">
                            {item.product.titleAr}
                          </h4>
                          <span className="text-[11px] text-[#059669] block mt-0.5">
                            {item.product.priceEGP} ج.م / للعبوة
                          </span>
                        </div>

                        {/* Quantity Counter */}
                        <div className="flex items-center gap-2 bg-white px-2 py-1 rounded-lg border border-[#e2ece6]">
                          <button
                            type="button"
                            onClick={() =>
                              onUpdateQuantity(item.product.id, Math.max(1, item.quantity - 1))
                            }
                            className="text-[#526058] hover:text-[#064e3b] cursor-pointer"
                          >
                            <Minus className="w-3.5 h-3.5" />
                          </button>
                          <span className="font-bold text-[#121c2a] w-5 text-center tabular-nums">
                            {item.quantity}
                          </span>
                          <button
                            type="button"
                            onClick={() =>
                              onUpdateQuantity(item.product.id, item.quantity + 1)
                            }
                            className="text-[#526058] hover:text-[#064e3b] cursor-pointer"
                          >
                            <Plus className="w-3.5 h-3.5" />
                          </button>
                        </div>

                        {/* Remove item button */}
                        <button
                          type="button"
                          onClick={() => onRemoveItem(item.product.id)}
                          className="text-[#707974] hover:text-[#ba1a1a] transition-colors p-1 cursor-pointer"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Delivery Details Form */}
              <form onSubmit={handleCheckout} className="space-y-4 pt-2 border-t border-[#e2ece6]">
                <h4 className="text-xs font-bold text-[#064e3b]">
                  بيانات الشحن والتوصيل للمنزل:
                </h4>

                {/* Name */}
                <div>
                  <label className="block text-xs font-bold text-[#121c2a] mb-1">
                    الاسم بالكامل (أو اسم مستلم الشحنة):
                  </label>
                  <input
                    type="text"
                    value={customerName}
                    onChange={(e) => setCustomerName(e.target.value)}
                    placeholder="مثال: ياسمين أحمد محمود"
                    className="w-full text-xs p-2.5 rounded-lg border border-[#e2ece6] focus:border-[#059669] focus:ring-1 focus:ring-[#059669]/20 outline-none text-right bg-white"
                  />
                  {formErrors.name && (
                    <span className="text-[11px] text-[#ba1a1a] block mt-1">
                      {formErrors.name}
                    </span>
                  )}
                </div>

                {/* Phone */}
                <div>
                  <label className="block text-xs font-bold text-[#121c2a] mb-1">
                    رقم الموبايل المصري (للتواصل والشحن):
                  </label>
                  <input
                    type="tel"
                    dir="ltr"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="01012345678"
                    className="w-full text-xs p-2.5 rounded-lg border border-[#e2ece6] focus:border-[#059669] focus:ring-1 focus:ring-[#059669]/20 outline-none font-mono text-right bg-white"
                  />
                  {formErrors.phone && (
                    <span className="text-[11px] text-[#ba1a1a] block mt-1">
                      {formErrors.phone}
                    </span>
                  )}
                </div>

                {/* Governorate */}
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="text-xs font-bold text-[#121c2a]">
                      المحافظة:
                    </label>
                    <span className="text-[11px] text-[#059669] font-medium">
                      {isFreeShipping ? 'شحن مجاني لكافة المحافظات' : `مصاريف الشحن: ${shippingFee} ج.م`}
                    </span>
                  </div>
                  <select
                    value={selectedGovId}
                    onChange={(e) => setSelectedGovId(e.target.value)}
                    className="w-full text-xs p-2.5 rounded-lg border border-[#e2ece6] focus:border-[#059669] outline-none text-right bg-white cursor-pointer"
                  >
                    {EGYPTIAN_GOVERNORATES.map((gov) => (
                      <option key={gov.id} value={gov.id}>
                        {gov.nameAr} ({gov.deliveryDaysAr})
                      </option>
                    ))}
                  </select>
                </div>

                {/* Address */}
                <div>
                  <label className="block text-xs font-bold text-[#121c2a] mb-1">
                    العنوان بالتفصيل:
                  </label>
                  <textarea
                    rows={2}
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    placeholder="اسم المنطقة، الشارع، رقم العمارة والدور والشقة، وأقرب علامة مميزة"
                    className="w-full text-xs p-2.5 rounded-lg border border-[#e2ece6] focus:border-[#059669] focus:ring-1 focus:ring-[#059669]/20 outline-none text-right bg-white"
                  />
                  {formErrors.address && (
                    <span className="text-[11px] text-[#ba1a1a] block mt-1">
                      {formErrors.address}
                    </span>
                  )}
                </div>

                {/* Delivery Notes */}
                <div>
                  <label className="block text-xs font-bold text-[#121c2a] mb-1">
                    ملاحظات للمندوب أو موعد الاستلام (اختياري):
                  </label>
                  <input
                    type="text"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="مثال: يرجى الاتصال قبل الوصول بنصف ساعة"
                    className="w-full text-xs p-2.5 rounded-lg border border-[#e2ece6] focus:border-[#059669] outline-none text-right bg-white"
                  />
                </div>

                {/* Payment Method Selector */}
                <div className="pt-2">
                  <label className="block text-xs font-bold text-[#064e3b] mb-2">
                    طريقة الدفع المعتمدة:
                  </label>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    {/* COD */}
                    <button
                      type="button"
                      onClick={() => setPaymentMethod('cod')}
                      className={`p-3 rounded-xl border text-right transition-all cursor-pointer ${
                        paymentMethod === 'cod'
                          ? 'border-[#059669] bg-[#f3f7f5] shadow-xs ring-1 ring-[#059669]/20'
                          : 'border-[#e2ece6] hover:border-[#bfc9c3] bg-white'
                      }`}
                    >
                      <div className="flex items-center gap-1.5 mb-1">
                        <CheckCircle2
                          className={`w-4 h-4 ${
                            paymentMethod === 'cod' ? 'text-[#059669]' : 'text-[#bfc9c3]'
                          }`}
                        />
                        <span className="text-xs font-bold text-[#064e3b]">
                          الدفع عند الاستلام (COD)
                        </span>
                      </div>
                      <span className="text-[11px] text-[#526058] block">
                        معاينة الشحنة قبل الدفع للمندوب
                      </span>
                    </button>

                    {/* InstaPay */}
                    <button
                      type="button"
                      onClick={() => setPaymentMethod('instapay')}
                      className={`p-3 rounded-xl border text-right transition-all cursor-pointer ${
                        paymentMethod === 'instapay'
                          ? 'border-[#059669] bg-[#f3f7f5] shadow-xs ring-1 ring-[#059669]/20'
                          : 'border-[#e2ece6] hover:border-[#bfc9c3] bg-white'
                      }`}
                    >
                      <div className="flex items-center gap-1.5 mb-1">
                        <CheckCircle2
                          className={`w-4 h-4 ${
                            paymentMethod === 'instapay' ? 'text-[#059669]' : 'text-[#bfc9c3]'
                          }`}
                        />
                        <span className="text-xs font-bold text-[#064e3b]">
                          تحويل عبر InstaPay
                        </span>
                      </div>
                      <span className="text-[11px] text-[#526058] block">
                        تحويل فوري لحظي بدون رسوم
                      </span>
                    </button>
                  </div>
                </div>

                {/* Price Breakdown */}
                <div className="p-3.5 rounded-xl bg-[#f8f9ff] border border-[#d9e3f6] space-y-1.5 text-xs">
                  <div className="flex justify-between text-[#526058]">
                    <span>قيمة المنتجات:</span>
                    <span className="tabular-nums font-semibold text-[#121c2a]">
                      {subtotal} ج.م
                    </span>
                  </div>
                  <div className="flex justify-between text-[#526058]">
                    <span>مصاريف الشحن:</span>
                    <span className="tabular-nums font-semibold text-[#059669]">
                      {shippingFee === 0 ? 'مجاني (عرض البروتوكول)' : `${shippingFee} ج.م`}
                    </span>
                  </div>
                  {hasBundle && (
                    <div className="flex justify-between text-[#ba1a1a]">
                      <span>توفير الباقة الشاملة:</span>
                      <span className="tabular-nums font-semibold">-400 ج.م</span>
                    </div>
                  )}
                  <div className="flex justify-between font-bold text-sm text-[#064e3b] pt-2 border-t border-[#d9e3f6]">
                    <span>الإجمالي المستحق:</span>
                    <span className="tabular-nums text-base text-[#059669]">
                      {total} ج.م
                    </span>
                  </div>
                </div>

                {/* Error message if cart empty */}
                {formErrors.cart && (
                  <div className="flex items-center gap-2 p-2.5 rounded-lg bg-[#ffdad6]/40 text-xs text-[#ba1a1a]">
                    <AlertCircle className="w-4 h-4 shrink-0" />
                    <span>{formErrors.cart}</span>
                  </div>
                )}

                {/* Submit Order Button */}
                <button
                  type="submit"
                  disabled={cart.length === 0}
                  className="w-full py-3.5 px-6 rounded-xl text-sm font-bold text-white bg-[#064e3b] hover:bg-[#003527] disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md active:scale-[0.99] cursor-pointer flex items-center justify-center gap-2"
                >
                  <ShieldCheck className="w-4 h-4 text-[#82f5c1]" />
                  <span>تأكيد الطلب الفوري ({total} ج.م)</span>
                </button>

                <p className="text-[11px] text-[#707974] text-center">
                  بمجرد تأكيد الطلب، سيتم تغليف منتجاتك في بيئة معقمة وإرسالها مع شركة الشحن المعتمدة.
                </p>
              </form>
            </>
          )}
        </div>

      </div>
    </div>
  );
};
