import React, { useState } from 'react';
import { Order } from '../types/protocol';
import { X, Search, PackageCheck, Clock, Truck, ShieldCheck, MapPin } from 'lucide-react';

interface OrderLookupModalProps {
  isOpen: boolean;
  onClose: () => void;
  orders: Order[];
}

export const OrderLookupModal: React.FC<OrderLookupModalProps> = ({
  isOpen,
  onClose,
  orders
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  if (!isOpen) return null;

  const filteredOrders = orders.filter(
    (o) =>
      o.orderNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
      o.phone.includes(searchTerm) ||
      o.customerName.includes(searchTerm)
  );

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-[#121c2a]/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="w-full max-w-xl bg-white rounded-2xl shadow-xl border border-[#e2ece6] overflow-hidden text-right animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="px-5 py-4 border-b border-[#e2ece6] flex items-center justify-between bg-[#fbfdfb]">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-[#059669]/10 text-[#059669] flex items-center justify-center">
              <PackageCheck className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-[#064e3b]">
                سجل طلباتي ومتابعة الشحن
              </h3>
              <p className="text-[11px] text-[#526058]">
                متابعة حالة تجهيز وتسليم بروتوكول القيصرية الخاص بك
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-[#707974] hover:bg-[#f3f7f5] transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-5 space-y-4 max-h-[75vh] overflow-y-auto">
          {/* Search box if there are multiple orders */}
          {orders.length > 1 && (
            <div className="relative">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="ابحثي برقم الطلب (مثال: HT-EG-1234) أو رقم الموبايل..."
                className="w-full text-xs p-2.5 pr-8 rounded-lg border border-[#e2ece6] focus:border-[#059669] outline-none text-right bg-[#fbfdfb]"
              />
              <Search className="w-4 h-4 text-[#707974] absolute right-2.5 top-3" />
            </div>
          )}

          {orders.length === 0 ? (
            <div className="py-12 text-center text-xs text-[#526058] bg-[#f3f7f5] rounded-xl border border-[#e2ece6] space-y-2">
              <p className="font-semibold text-sm text-[#064e3b]">لم يتم تسجيل أي طلبات سابقة على هذا الجهاز</p>
              <p>عند إتمامك لأي طلب، ستتمكنين من متابعة حالة التجهيز والشحن هنا فوراً.</p>
            </div>
          ) : filteredOrders.length === 0 ? (
            <div className="py-8 text-center text-xs text-[#526058]">
              لا توجد نتائج مطابقة لبحثك.
            </div>
          ) : (
            <div className="space-y-4">
              {filteredOrders.map((order) => (
                <div
                  key={order.id}
                  className="p-4 rounded-xl border border-[#e2ece6] bg-[#fbfdfb] space-y-3"
                >
                  {/* Top Bar */}
                  <div className="flex items-center justify-between border-b border-[#e2ece6] pb-2.5">
                    <div>
                      <span className="font-mono text-xs font-bold text-[#064e3b]">
                        {order.orderNumber}
                      </span>
                      <span className="text-[11px] text-[#707974] block mt-0.5">
                        {new Date(order.createdAt).toLocaleDateString('ar-EG', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </span>
                    </div>

                    <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#82f5c1]/20 text-[#006c4a] text-xs font-bold">
                      <Truck className="w-3.5 h-3.5" />
                      <span>{order.status === 'confirmed' ? 'تم التأكيد وجارٍ التجهيز' : 'في الطريق للشحن'}</span>
                    </div>
                  </div>

                  {/* Customer info */}
                  <div className="text-xs text-[#404944] space-y-1">
                    <div className="flex justify-between">
                      <span className="text-[#707974]">المستلم:</span>
                      <span className="font-bold text-[#121c2a]">{order.customerName} ({order.phone})</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-[#707974] flex items-center gap-1">
                        <MapPin className="w-3 h-3 text-[#059669]" />
                        <span>محافظة التوصيل:</span>
                      </span>
                      <span className="font-semibold text-[#121c2a]">{order.governorate} - {order.address}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-[#707974]">طريقة الدفع:</span>
                      <span className="font-semibold text-[#064e3b]">
                        {order.paymentMethod === 'cod' ? 'الدفع عند الاستلام' : 'إنستاباي (InstaPay)'}
                      </span>
                    </div>
                  </div>

                  {/* Items list */}
                  <div className="bg-white p-2.5 rounded-lg border border-[#e2ece6] space-y-1.5 text-xs">
                    {order.items.map((it, idx) => (
                      <div key={idx} className="flex justify-between text-[#121c2a]">
                        <span>
                          {it.titleAr} × <strong className="tabular-nums font-mono">{it.quantity}</strong>
                        </span>
                        <span className="tabular-nums font-semibold text-[#059669]">
                          {it.priceEGP * it.quantity} ج.م
                        </span>
                      </div>
                    ))}
                    <div className="pt-2 border-t border-[#e2ece6] flex justify-between font-bold text-xs text-[#064e3b]">
                      <span>الإجمالي المدفوع / المستحق:</span>
                      <span className="text-sm font-extrabold text-[#059669] tabular-nums">
                        {order.totalEGP} ج.م
                      </span>
                    </div>
                  </div>

                  <div className="text-[11px] text-[#526058] flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-[#059669]" />
                    <span>موعد التسليم المتوقع: {order.estimatedDeliveryAr}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 bg-[#f8f9ff] border-t border-[#e2ece6] text-center">
          <button
            onClick={onClose}
            className="px-6 py-2 rounded-lg text-xs font-semibold text-[#064e3b] bg-white border border-[#e2ece6] hover:bg-[#f3f7f5] transition-colors cursor-pointer"
          >
            إغلاق النافذة
          </button>
        </div>

      </div>
    </div>
  );
};
