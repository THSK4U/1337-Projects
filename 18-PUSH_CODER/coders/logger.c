/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   logger.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 08:40:10 by Tsellak           #+#    #+#             */
/*   Updated: 2026/06/29 08:42:11 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	ft_exit(const char *format, const void *arg1, const void *arg2)
{
	printf(format, arg1, arg2);
	exit(1);
}

void	log_action(t_coder *coder, const char *message)
{
	long	time_now;

	pthread_mutex_lock(&coder->data->print_mutex);
	time_now = get_time_ms() - coder->data->start_time;
	printf("%ld %d %s\n", time_now, coder->id, message);
	pthread_mutex_unlock(&coder->data->print_mutex);
}
