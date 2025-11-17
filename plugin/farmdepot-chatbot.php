<?php
/**
 * Plugin Name: FarmDepot Multilingual Chatbot
 * Description: AI chatbot integrating FarmDepot with N-ATLaS LLM API.
 */

if (!defined('ABSPATH')) exit;

// Enqueue JS file
add_action("wp_enqueue_scripts", "farmdepot_chatbot_assets");
function farmdepot_chatbot_assets() {
    
    // Load JS
    wp_enqueue_script(
        "farmdepot-chat",
        plugin_dir_url(__FILE__) . "farmdepot-chat.js",
        ['jquery'],
        null,
        true
    );

    // Pass AJAX URL to JS
    wp_localize_script(
        "farmdepot-chat",
        "farmdepot_ajax",
        [
            "ajax_url" => admin_url("admin-ajax.php")
        ]
    );
}


// AJAX endpoint for logged-in and guest users
add_action('wp_ajax_farmdepot_ai_chat', 'farmdepot_ai_chat');
add_action('wp_ajax_nopriv_farmdepot_ai_chat', 'farmdepot_ai_chat');

function farmdepot_ai_chat() {

    $message = sanitize_text_field($_POST['message']);
    $language = sanitize_text_field($_POST['language']);

    $api_url = "https://YOUR-SERVER-IP:8000/chat";

    $body = json_encode([
        "message" => $message,
        "language" => $language
    ]);

    $response = wp_remote_post($api_url, [
        'headers' => ["Content-Type" => "application/json"],
        'body' => $body,
        'timeout' => 30
    ]);

    if (is_wp_error($response)) {
        wp_send_json_error(["error" => "Server error"]);
    }

    $data = json_decode(wp_remote_retrieve_body($response), true);
    wp_send_json_success($data);
}

add_shortcode('farmdepot_chatbot', function () {
    ob_start();
    ?>
    <div id="chatBox" style="border:1px solid #ccc;padding:10px;height:300px;overflow-y:auto;"></div>

    <select id="langSelect" style="margin-top:10px;">
        <option value="en">English</option>
        <option value="ha">Hausa</option>
        <option value="yo">Yoruba</option>
        <option value="ig">Igbo</option>
    </select>

    <input type="text" id="chatInput" placeholder="Type your message..." style="width:70%;margin-top:10px;" />
    <button id="sendBtn">Send</button>
    <?php
    return ob_get_clean();
});