package mx.tec.vanttec.dron

import dji.common.error.DJIError
import dji.sdk.base.BaseProduct
import dji.sdk.sdkmanager.DJISDKManager.SDKManagerCallback
import io.reactivex.Observable
import io.reactivex.ObservableEmitter
import io.reactivex.ObservableOnSubscribe
import io.reactivex.subjects.SingleSubject

class SDKManagerCallback : SDKManagerCallback, ObservableOnSubscribe<BaseProduct> {

    val registerSubject = SingleSubject.create<DJIError>()
    val productObservable = Observable.create(this).publish()!!

    private var observableEmitter: ObservableEmitter<BaseProduct>? = null

    init {
        productObservable.connect()
    }

    override fun onRegister(error: DJIError?) {
        if(error != null)
            registerSubject.onSuccess(error)
        else
            registerSubject.onError(Exception("Register failed"))
    }

    override fun onProductChange(oldProduct: BaseProduct?, newProduct: BaseProduct?) {
        if(newProduct != null)
            observableEmitter?.onNext(newProduct)
        else
            observableEmitter?.onError(Exception("Product disconnected"))
    }

    override fun subscribe(emitter: ObservableEmitter<BaseProduct>) {
        observableEmitter = emitter
    }
}