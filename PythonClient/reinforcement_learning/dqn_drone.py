# 導入所需的套件和函式庫
import setup_path
import gym
import airgym
import time

from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecTransposeImage
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback

# 創建一個虛擬環境（DummyVecEnv）以用於 AirSim 飛行模擬器
env = DummyVecEnv(
    [
        lambda: Monitor(
            gym.make(
                "airgym:airsim-drone-sample-v0",  # 使用的 gym 環境
                ip_address="127.0.0.1",  # AirSim 伺服器的 IP 地址
                step_length=0.25,  # 每個步驟的長度
                image_shape=(100, 80, 1),  # 觀察到的圖像形狀
            )
        )
    ]
)

# 使用 VecTransposeImage 包裝環境，使其適合處理框架觀察
env = VecTransposeImage(env)

# 初始化深度 Q 網絡 (DQN) 模型和其參數
model = DQN(
    "CnnPolicy",  # 使用的策略網絡類型
    env,
    learning_rate=0.00025,  # 學習率
    verbose=1,
    batch_size=32,  # 批量大小
    train_freq=4,  # 訓練頻率
    target_update_interval=10000,  # 目標網絡更新間隔
    learning_starts=10000,  # 開始學習前的時間步數
    buffer_size=500000,  # 經驗重放緩衝區的大小
    max_grad_norm=10,  # 梯度裁剪的最大值
    exploration_fraction=0.1,  # 探索階段的比例
    exploration_final_eps=0.01,  # 探索的最終概率
    device="cuda",  # 使用的設備（例如 CUDA）
    tensorboard_log="./tb_logs/",  # TensorBoard 日誌的儲存路徑
)

# 創建一個評估回調，每 10000 次迭代時使用相同的環境進行評估
callbacks = []
eval_callback = EvalCallback(
    env,
    callback_on_new_best=None,
    n_eval_episodes=5,  # 評估時的遊戲回合數
    best_model_save_path=".",  # 最佳模型儲存路徑
    log_path=".",  # 日誌路徑
    eval_freq=10000,  # 評估頻率
)
callbacks.append(eval_callback)

# 額外的關鍵字參數設置
kwargs = {}
kwargs["callback"] = callbacks

# 開始訓練模型，設置訓練的總時間步數
model.learn(
    total_timesteps=5e5,  # 總時間步數
    tb_log_name="dqn_airsim_drone_run_" + str(time.time()),  # TensorBoard 日誌的名稱
    **kwargs  # 使用前面定義的關鍵字參數
)

# 訓練結束後，保存模型的權重
model.save("dqn_airsim_drone_policy")