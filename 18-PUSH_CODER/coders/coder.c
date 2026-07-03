/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 08:39:57 by Tsellak           #+#    #+#             */
/*   Updated: 2026/06/29 10:46:59 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	coder_phase(t_coder *coder, const char *msg, long ms)
{
	log_action(coder, msg);
	return (sleep_until_or_burnout(coder, ms));
}

static int	handle_compile_phase(t_coder *coder)
{
	if (simulation_check(coder->data))
		return (0);
	while (!take_two_dongles(coder))
	{
		if (simulation_check(coder->data) || get_time_ms() >= coder->deadline)
			return (0);
		usleep(500);
	}
	pthread_mutex_lock(&coder->state_mutex);
	coder->last_compile_start = get_time_ms();
	coder->deadline = coder->last_compile_start + coder->data->time_to_burnout;
	pthread_mutex_unlock(&coder->state_mutex);
	if (!coder_phase(coder, "is compiling", coder->data->time_to_compile))
	{
		release_two_dongles(coder);
		return (0);
	}
	release_two_dongles(coder);
	return (1);
}

void	*coder_routine(void *arg)
{
	t_coder	*coder;
	int		done;

	coder = (t_coder *)arg;
	done = 0;
	while (!done)
	{
		pthread_mutex_lock(&coder->state_mutex);
		done = (coder->compile_count >= coder->data->num_compiles_required);
		pthread_mutex_unlock(&coder->state_mutex);
		if (done)
			break ;
		if (!handle_compile_phase(coder))
			return (NULL);
		if (!coder_phase(coder, "is debugging", coder->data->time_to_debug))
			return (NULL);
		if (!coder_phase(coder, "is refactoring",
				coder->data->time_to_refactor))
			return (NULL);
		pthread_mutex_lock(&coder->state_mutex);
		coder->compile_count++;
		pthread_mutex_unlock(&coder->state_mutex);
	}
	return (NULL);
}
